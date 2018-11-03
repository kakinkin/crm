from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_POST,require_GET
from .models import User
from django.http import  JsonResponse
from email.header import   Header# 如果包含中文，需要通过Header对象进行编码
from email.mime.text import  MIMEText
from email.utils import  parseaddr,formataddr
import smtplib
import  uuid
from datetime import  datetime,timedelta
from hashlib import  md5
import base64

# Create your views here.

#跳转到登录和注册页面
def login_register(request):
    return render(request, 'system/login_register.html')


# 验证用户名是否唯一,并返回响应状态码对应的提示信息给前台
@require_POST
def unique_username(request):
    try:
    # 接收参数
        username=request.POST.get('username')
    # 查询是否有该用户，如果不存在，可能汇报异常，也可参考get_or_方法？
        user=User.objects.get(username=username)
        user_name=user.username
    # 有用户返回页面json
        context={'code': 400, 'msg': '用户名已存在','user_name':username}
        return JsonResponse(context)
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '用户名可以使用'})

@require_POST
def unique_email(request):
    try:
        # 接收参数
        email=request.POST.get('email')

        #查询是否有该用户
        user=User.objects.get(email=email)
        user_email=user.email
        # 有用户返回页面json
        return JsonResponse({'code':400, 'msg':'邮箱已经存在','user_email':user_email})
    except User.DoesNotExist as e:
        return JsonResponse({'code':200,'msg':'可以使用该邮箱'})


# -----------------email模块构建邮件发送实体对象--------------
# 格式化邮箱(不格式化会被当做垃圾邮件去发送或者发送失败)
def format_addr(s):
    name, addr = parseaddr(s)  # 比如：尚学堂 <java_mail01@163.com>
    # 因为name可能会有中文，需要对中文进行编码
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))

# 邮件发送
@require_POST
def send_email(request):
    try:
     # --------------------------准备数据-------------start-------------
        # 发送邮箱
        from_addr='jjjkauau@126.com'
        # 程序代码中登录的密码其实就是那个你设置的授权码
        password='jjjkauau126'
        # 发送服务器
        smtp_server="smtp.126.com"
        # 接收邮箱
        to_addr=request.POST.get('email')

        #邮箱截取


        #用户名
        username=request.POST.get('username')
        #密码
        u_pwd=request.POST.get('password')
        #使用md5加密
        u_pwd = md5(u_pwd.encode(encoding='utf-8')).hexdigest()
        print(u_pwd,type(u_pwd))
        #激活码
        code=''.join(str(uuid.uuid4()).split('-'))
        # 10分钟后的时间戳
        td=timedelta(minutes=10)
        ts=datetime.now()+td
        # print(ts,type(ts))
     #<class 'datetime.datetime'>
        ts=str(ts.timestamp()).split('.')[0]

     # --------------------------准备数据---------------end-----------

     # -----------------------插入数据库数据----------start--------------
        user = User(username=username, password=u_pwd, email=to_addr, code=code, timestamp=ts)
        user.save()
        # -----------------------插入数据库数据----------end--------------

        # ------------------------构建邮件内容对象----------start--------------
        html = """
                          <html>
                              <body>
                                  <div>
                                  Email 地址验证<br>
                                  这封信是由 上海尚学堂 发送的。<br>
                                  您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br>
                                  如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                                  ----------------------------------------------------------------------<br>
                                   帐号激活说明<br>
                                  ----------------------------------------------------------------------<br>
                                  如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                                  您只需点击下面的链接激活帐号即可：<br>
                                  <a href="http://www.justin.com/system/active_accounts/?username={}&code={}&timestamp={}">http://www.justin.com/system/active_accounts/?username={}&amp;code={}&amp;timestamp={}</a><br/>
                                  感谢您的访问，祝您生活愉快！<br>
                                  此致<br>
                                   上海尚学堂 管理团队.
                                  </div>
                              </body>
                          </html>
                       """.format(username, code, ts, username, code, ts)
        msg = MIMEText(html, "html", "utf-8")

        # 标准邮件需要三个头部信息： From To 和 Subject
        # 设置发件人和收件人的信息 u/U:表示unicode字符串
        # 比如：尚学堂 <java_mail01@163.com>
        msg['From'] = format_addr(u'尚学堂<%s>' % from_addr)  # 发件人
        to_name = username  # 收件人名称
        msg['To'] = format_addr(u'{}<%s>'.format(to_name) % to_addr)  # 收件人

        # 设置标题
        # 如果接收端的邮件列表需要显示发送者姓名和发送地址就需要设置Header，同时中文需要encode转码
        msg['Subject'] = Header(u'CRM系统官网帐号激活邮件', 'utf-8').encode()
        # ------------------------构建邮件内容对象-----------end-------------

        # ------------------------------发送--------------start----------------
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(smtp_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)
        # 登录发件邮箱
        server.login(from_addr, password)
        # 调用发送方法 第一个参数是发送者邮箱，第二个是接收邮箱，第三个是发送内容
        server.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭发送
        server.quit()
        # ------------------------------发送----------------end--------------

        # 返回页面提示信息
        return JsonResponse({'code': 201, 'msg': '注册成功，请前往邮箱激活帐号'})

    except smtplib.SMTPException as e:
    # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '注册失败，请重新注册！'})

 #其中get内含有键值对的参数包括username,激活码  ，过期的时间戳字符串
@require_GET
def active_accounts(reqeuest):
    try:
        #用户名
        username=reqeuest.GET.get('username')
        #激活码
        code=reqeuest.GET.get('code')
        #过期时间
        ts=reqeuest.GET.get('timestamp')
        #根据用户和激活码查询是否有该账号
        user=User.objects.get(username=username,code=code,timestamp=ts)
        # 根据过期时间判断帐号是否有效
        now_ts = str(datetime.now().timestamp()).split('.')[0]
        if int(now_ts)>int(ts):
            # 链接失效，返回提示信息，删除数据库信息
            user.delete()
            return HttpResponse('<h1>该链接已经失效，请重新注册&nbsp;&nbsp;<a href="http://www.justin.com/login_register/"上海丽特CRM系统</a></h1>')
        #没有过期，激活账号，清除激活码，改变状态
        user.code='' #清除激活码
        user.status=1 #有效账号
        user.save()
        # 返回提示信息
        return HttpResponse(
            '<h1>账号激活成功，请到网系统登录&nbasp;&nbsp;<a href="http://www.justin.com/login_register/">上海丽特CRM系统</a></h1>'

        )
    except Exception as e:
        if isinstance(e,User.DoesNotExist):
            return HttpResponse('<h1>该链接已经失效，请重新注册&nbsp;&nbsp;<a href="http://www.justin.com/login_register/">上海丽特CRM系统</a></h1>')
        return HttpResponse('<h1>不好意思，网络出现了波动，激活失败，请重新尝试</h1>')


# 登录

@require_POST

def login_user(request):
    try:
        #接收前台传来的数据
        # 账号
        username=request.POST.get('username')
        #密码
        password=request.POST.get('password')
        #记住密码

        remeber=request.POST.get('remember')
        print(remeber,type(remeber))

        #5天免登录
        login_free = request.POST.get('login_free')

        forgot_pwd=request.POST.get('forgot_pwd')

        # 使用md5加密
        password_md5=md5(password.encode(encoding='utf-8')).hexdigest()

        #查询
        user=User.objects.get(username=username,password=password_md5)

        # 如果用户存在，存储sesison信息

        request.session['u_s_n']=username

        #如果选选择存储5天的sesison，没选择浏览器关闭session失效
        if  login_free:
            ex=(datetime.now()+timedelta(days=6)).timestamp()
            request.session.set_expiry(ex)
        else:
            request.session.set_expiry(0)




        # 返回成功提示信息
        context={'code':200,'msg':'欢迎回来'}

        # 实现记住密码
        # 如果用户存在，前台js存储cookie
        # 存储格式：key -> login_cookie, value -> username&password
        # 由于功能改造，代码重构
        if 'true' == remeber:
           # context['login_cookie'] = base64.b64encode((username + '&' + password).encode(encoding='utf-8')).decode(encoding='utf-8')
           context['login_user_cookie'] = base64.b64encode(username.encode(encoding='utf-8')).decode(encoding='utf-8')
           context['login_pwd_cookie'] = base64.b64encode(password.encode(encoding='utf-8')).decode(encoding='utf-8')

        # #实现忘记密码功能
        # if format_addr:
        #     return render(request,'forgot.html.html')

        return JsonResponse(context)


    except User.DoesNotExist as e:
        context={'code':400,'msg':'用户名或密码错误'}
        return JsonResponse(context)



def index(request):
        # 判断session中是否有用户信息
        username=request.session.get('u_s_n')

        if username:
            return render(request, 'system/index1.html')
        # 如果不存在，重定向登录页面
        return redirect('system:login_register',permanent=True)




#修改密码
@require_POST
def update_password(request):
    try:
        username=request.POST.get('username')
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')

        #使用md5加密
        old_password_md5=md5(old_password.encode(encoding='utf-8')).hexdigest()

        # 查询用户密码是否正确
        user=User.objects.get(username=username,password=old_password)

        #使用md5加密
        new_password_md5=md5(new_password.encode(encoding='utf-8')).hexdigest()


        #修改密码
        user.password=new_password_md5
        user.save()

        # 修改密码要重新登录，所以要安全退出
        # 安全退出系统要清除session，所以这里不写
        return JsonResponse({'code':200,'msg':'修改成功'})
    except User.DoesNotExist as e:
        return  JsonResponse({'code':400,'msg':'原密码输入错误'})

    #安全退出

def logout(request):
        try:
            #清除session
            request.session.flush()

            #重定向到登录页面
            return  redirect('system:login_register')
        except Exception as e:
            #重定向至登录页面
            return  redirect('system:login_register')
from django.shortcuts import render
import pymysql
from dbutils import  pymysql_pool
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import  Paginator
from django.views.decorators.csrf import  csrf_exempt
from sales.models import SaleChance
from datetime import  datetime



# 准备数据
config = {
    'host': 'localhost',  # 数据库ip
    'port': 3306,  # 数据库用户名
    'user': 'root',  # 数据库密码
    'password': '123456',  # 数据库端口
    'database': 'crm',  # 具体的一个库 等价于database
    'charset': 'utf8mb4',  # 字符集
    # 默认获取的数据是元祖类型，如果想要或者字典类型的数据
    'cursorclass': pymysql.cursors.DictCursor
}

#初始化连接池对象
connect_pool=pymysql_pool.ConnectionPool(size=50,name='mysql_pool',**config)


#从数据库连接池中获取连接
def connect():
    #从连接池中获取连接
    connection=connect_pool.get_connection()
    return  connection


def sale_chance_index(request):
    '''跳转营销机会首页'''
    return  render(request,'sales/sale_chance.html')

@csrf_exempt
@require_POST
def select_sale_chance_list(request):
    '''查询所有营销机会'''
    try:
        #获取第几页
        page_num=request.POST.get('page')

        #获取每页多少条
        page_size=request.POST.get('rows')

        #获取连接
        connection=connect()

        #创建游标对象
        cursor=connection.cursor()

        #编写sql
        sql='''
               SELECT
                    sc.id id,
                    c.id customerId, 
                    c.khno khno,
                    c.name customerName,
                    sc.overview overview,
                    sc.create_man createMan,
                    cl.id linkManId,
                    cl.link_name linkManName,
                    cl.phone linkPhone,
                    u.user_name assignMan,
                    sc.assign_time assignTime,
                    sc.state state,
                    sc.dev_result devResult
                    FROM
                        t_sale_chance sc
                LEFT JOIN t_customer c ON sc.customer_id = c.id
                LEFT JOIN t_user u ON u.id = sc.assign_man
                LEFT JOIN t_customer_linkman cl ON cl.id = sc.link_man
                WHERE 1 = 1        
            '''

        #如果用户选择了其他条件，拼接sql
        #客户名称
        customerName=request.POST.get('cn')
        #概要
        overview=request.POST.get('ow')
        # 创建人
        creatman=request.POST.get('cm')
        # 分配状态
        state = request.POST.get('st')

        if customerName:
            sql+='  AND c.name like "%{}%"  '.format(customerName)

        if overview:
            sql+='  AND sc.overview like "%{}%"  '.format(overview)

        if creatman:
            sql+='  AND sc.create_man like "%{}%"  '.format(creatman)

        if state:
            sql+=' AND sc.state = {}   '.format(state)


        sql+='  ORDER BY sc.id DESC; '

        #执行sql
        cursor.execute(sql)

        #返回多条结果行
        object_lists=cursor.fetchall()  #查询当前sql执行后所有记录

        #关闭游标
        cursor.close()

        #初始化分页对象
        p=Paginator(object_lists,page_size)

        #获取指定页数的数据
        data=p.page(page_num).object_list

        #返回总条数
        count=p.count

        #返回数据
        context={
            'total':count,
            'rows':data
        }

        return JsonResponse(context)

    except Exception as e:
        print(e)
        return JsonResponse({'code':400,'msg':'error'})

    finally:
        #关闭游标连接
        connection.close()



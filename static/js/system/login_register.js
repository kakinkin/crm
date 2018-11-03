// ----------------------------------注册------------start----------------------



$(function () {
    $('#reg_top').on('click', function () {

    $('#log-in').hide();
    $('#register').show();
});

// 点击登录将注册div隐藏，显示登录div，注意代码执行顺序
$('#login_top').on('click', function () {

    $('#register').hide();
    $('#log-in').show();
});

});


//组织重复数据
function show_btn() {
    $('#reg_btn').val('单击注册');
    $('#reg_btn').removeAttr('disabled');
};

function stop_btn() {
    $('#reg_btn').val('重复信息不能注册');
     $('#reg_btn').prop("disabled", "true");
};

    //非空通用方法,可能有三种情况
    function isEmpty(str) {
        if (undefined == str || '' == str || null == str) {
            return true;
        }
        return false;
    }

    var flag = false;

    // 验证用户名 丢失焦点事件,必须字母加数字
    function checke_username() {


        var reg = /^[a-zA-Z][a-zA-Z0-9]{3,15}$/

        // 获取用户名
        var uname = $('#reg_uname').val().trim();
        // 非空判断有三种情况

        if (isEmpty(uname)) {
            $('#reg_span').html('用户名不能为空');

            flag = false;

        }

        // 验证用户名 字母或者字母加数字必须字母开头 最少4位 最多16位

        else if (!reg.test(uname)) {
            $('#reg_span').html('用户名必须是字母开头，4~16位');
            flag = false;

        }

        // 发送ajax请求验证用户名唯一
        else {
            // 合法后清空提示
            $('#reg_span').html('');


            $.ajax({
                'type': 'POST',
                'url':'/system/unique_username/',
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'username': uname
                },
                'dataType': 'json',
                'success': function (result) {
                    // 如果是400 设置为false返回
                    if (400 == result.code) {

                        $('#reg_span').html(result.msg);
                        if (result.user_name==uname){
                       stop_btn();
                    }
                        flag = false;
                    }
                    else if (200 == result.code) {
                        $('#reg_span').html(result.msg);

                        show_btn();
                        flag = true;
                    }


                },
                'error': function (result) {
                    console.log(result);


                }

            });
        }


        return flag;

    }

    $('#reg_uname').on('blur', checke_username);


    // 验证邮箱
    function checke_email() {



        //邮箱正则,数字字母下划线或是中划线.号，
        var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;


        // 获取邮箱
        var email = $('#reg_email').val().trim();

        // 非空判断有三种情况
        if (isEmpty(email)) {
            $('#reg_span').html('邮箱不能为空');

            flag = false;

        }

        // 验证用户名 字母或者字母加数字必须字母开头 最少4位 最多16位

        else if (!reg.test(email)) {
            $('#reg_span').html('请输入正确邮箱格式');
            flag = false;

        }

        // 发送ajax请求验证邮箱名唯一
        else {
            //如果上边的两种不合法的情况没有出现即视为正常输入清空提示消息
            $('#reg_span').html('');


            $.ajax({
                'type': 'POST',
                'url':'/system/unique_email/',

                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'email': email
                },
                'dataType': 'json',
                'success': function (result) {
                    // 如果是400 设置为false返回
                    if (400 == result.code) {

                        if (result.user_email==email){
                            stop_btn();

                    }
                        $('#reg_span').html(result.msg);
                        flag = false;
                    }
                    else if (200 == result.code) {
                       // $('#reg_span').html(result.msg);
                        show_btn();

                        flag = true;
                    }


                },
                'error': function (result) {
                    console.log(result);


                }

            });
        }


        return flag;

    }


    $('#reg_email').on('blur', checke_email);


    // 判断一个字符串长度是否在某个区间  true-> 在此区间   false->不在此区间
    function str_length(str, min, max) {
        if (!(str.length < min || str.length > max)) {
            return true;
        }
        return false;
    }


    // 验证密码 必须数字大小写字母特殊符号组成 最少8位 最多16位
    function check_password() {

        var flag = false;
        //获取密码
        var pwd = $('#reg_pwd').val().trim();

        // 验证密码
        var reg = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;

        //非空校验
        if (isEmpty(pwd)) {
            $('#reg_span').html('密码不能为空');
            flag = false;
        }

        //判断密码长度
        else if (!str_length(pwd)) {
            $('#reg_span').html('密码长度必须在8~16位之间');
            flag = false;

        } else if (!reg.test(pwd)) {
            $('#reg_span').html('必须数字大小写字母特殊符号组成');
            flag = false;
        } else {
            $('#reg_span').html('');


            flag = true;
        }
        return flag;
    }

    $('#reg_pwd').on('blur', check_password);

    // 重复密码 获取密码的值进行比较
    function repeat_password2() {
        //获取密码
        var pwd = $('#reg_pwd').val().trim();
        //获取重复密码
        var pwd2 = $('#confirm_password').val().trim();

        //非空判断
        if (isEmpty(pwd2)) {
            $('#reg_span').html('重复密码不能为空');
            flag = false;

            // 进行比较
        } else if (pwd != pwd2) {
            $('#reg_span').html('两次密码不一致');
            flag = false;


        } else {

            // 合法后清空提示
            $('#reg_span').html('');
            flag = true;

        }
        return flag;
    }

    $('#confirm_password').on('blur', repeat_password2);



    // 点击注册按钮再次验证数据合法性,防止恶意注册

    $('#reg_btn').on('click', function () {

         // 点击注册以后置灰按钮
        $('#reg_btn').attr("disabled", "true");

        var flag1 = checke_username();
        var flag2 = checke_email();
        var flag3 = check_password();
        var flag4 = repeat_password2();
       if ((flag1&&flag2&&flag3&&flag4)){

            $('#reg_span').html('');
            var inputs=$('input');
               for (var i=0;i<inputs.length;i++){
                inputs[i].disabled=true;
           }


            // 合法的话 发送邮件 激活账号
        // 获取用户名
        var username = $('#reg_uname').val().trim();
        //获取邮箱
        var email = $('#reg_email').val().trim();
        //获取密码
        var password = $('#reg_pwd').val().trim();


        //异步实现邮件发送
        $.ajax({
            'type': 'POST',
            'url': '/system/send_email/',
            'data': {
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
                'email': email,
                'username': username,
                'password': password
            },
            'dataType': 'json',
            'success': function (result) {

                // 如果是400 设置为false返回
                if (400 == result.code) {
                    $('#reg_span').html(result.msg);
                    setTimeout("location.reload()",5000);


                }

                // 如果是200 正常显示
                if (201 == result.code) {

                    $('#reg_span').html(result.msg);
                }
            },
            'error': function (result) {
                console.log(result);
            }
        });
       }

        else {

              $('#reg_span').html('无法注册，请逐一检查，确保输入合法信息');
            return;
        }

    });

// ----------------------------------登录--------------start--------------------
// 用户名非空验证
function login_username() {
    username=$('#login_username').val().trim();
    if(isEmpty(username)){
           $('#login_span').html('请输入用户名');
           return false;
    }

    $('#login_span').html('');
    return true;

}

$('#login_username').on('blur',login_username);

function login_password() {
    password=$('#login_password').val().trim();
    if (isEmpty(password)){
           $('#login_span').html('请密码');
           return false;
    }

      $('#login_span').html('');
    return true;

}

$('#login_password').on('blur',login_password);

//登录点击事件
$('#login_btn').on('click',function () {
    alert("登录提交");
    var forgot_pwd=$('#forgot_pwd');



    var flag1=login_username();
    var flag2=login_password();
    if(!(flag1&&flag2)){
        return;
    }
    else {
    //如果输入合法
    var username=$('#login_username').val().trim();
    var password=$('#login_password').val().trim();
    var remember=$('#remember').is(':checked');
    var login_free=$('#login_free').is(':checked');
    //登录将值传给后台函数处理
    $.ajax({
        'type':'POST',
        'url':'/system/login_user/',
        'data':{
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username,
            'password':password,
            'remember':remember,
            'login_free':login_free


        },
        'dataType':'json',
        'success':function (result) {

             // 如果是400 显示错误信息
            if (400 == result.code) {
                $('#login_span').html(result.msg);

            }
            if(200==result.code){

                console.log(result);
                // 如果用户选择了记住密码
                if (!(undefined == result.login_user_cookie || null == result.login_user_cookie)){
                     // 设置cookuie，有效时间为15天
                  $.cookie('login_user_cookie',result.login_user_cookie, {'expires':5,'path':'/','domain':'www.justin.com'});
                  $.cookie('login_pwd_cookie',result.login_pwd_cookie, {'expires':5,'path':'/','domain':'www.justin.com'});
                }

               window.location.href='/index/';
            }

        },
        'error':function (result) {
            console.log(result);

        }

    });
    }

});


// 进入页面返现账号密码就执行的方法

$(function () {

      // 获取login_cookie，赋值到登录框
    var uname=$.cookie('login_user_cookie');
    var pwd=$.cookie('login_pwd_cookie')
// 判断是否存在cookie
    if(!(undefined==uname||null==uname)){
        // base64解密cookie
        uname=$.base64.decode(uname);
        // 赋值到登录框
        $('#login_username').val(uname);


    }


     if(!(undefined==pwd||null==pwd)){
        // base64解密cookie
        pwd=$.base64.decode(pwd);
        // 赋值到登录框
        $('#login_password').val(pwd);


    }


});








// 初始化修改密码dialog
$('#system_index_update_password_dialog').dialog({
    title:'修改密码',
    iconCls:'icon-edit',
    resizable:false,
    modal:true,//模态
    draggable:false,//不可移动
    closed:true,//是否关闭
    width:260,
    buttons:[{//按钮
        text:'保存',
        iconCls: 'icon-save',
        handler:function () {

            //做表单字段验证，当所有字段都有效的时候返回true。该方法使用validatebox(验证框)插件。
            var flag=$('#system_index_update_password_form').form('validate');
            console.log(flag);
            if(flag){
                //提交表单
                sub_system_index_updatepwd_form();

                //清除form表单inpt
                $('#system_index_update_password_form input').val();

                //关闭修改密码dialog
                $('#system_index_update_password_dialog').dialog('close');
            }

        }
    },{
        text:'关闭',
        iconCls:'icon-cancel',
        handle:function () {
            $('#system_index_update_password_dialog').dialog('close');

        }

    }]

});

//点击修改密码弹出对话框
function open_update_password_dialog(username) {
    //返显用户名
    $('#username').val(username);
    $('#system_index_update_password_dialog').dialog('open');

}



// 提交修改密码表单
function sub_system_index_updatepwd_form() {
//给csrf_token隐藏域复制
    $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));
    $('#system_index_update_password_form').form('submit',{
        url:'/system/update_password/',
        success:function (result) {
            // console.log(result);
            var obj=JSON.parse(result);
                // 显示提示信息
            $.messager.show({
                title: '提示',
                msg:obj.msg,
                timeout:5000
            });

              // 退出系统，清除cookie，清除session
            if(200==obj.code){
                //前台清除cookie   清除所有之前的cookie
                //$.removeCookie('login_user_cookie',{'expires':5,'path':'/','domain':'www.justin.com'});
                // 后台清除session
                   // 为了保证用户可以看到提示信息(修改成功或失败)，我们要延迟执行
                setTimeout(function () {
                    window.location='/system/logout/';

                },2000);

            }

        }


    });

}



// 安全退出 后台清除session
function logot() {
    //弹出提示框是否退出  r为
    $.messager.confirm('是否退出','您确认要退出系统么？',function (r) {
        if(r){
              // 清除cookie保留用户名
            console.log(r+"这是");
            $.removeCookie('login_pwd_cookie',{'expires':5,'path':'/','domain':'www.justin.com'});


            // 请求后台
            window.location.href = '/system/logout/';

        }

    })

}

//打开一一个新的tab页面，其实就是在中间div欢迎界面嵌套和展示页面
function openTab(title,url,iconCls) {
     // 中间div选项面板是否存在，存在选中，不存在添加
    var flag=$('#tabs').tabs('exists',title);
    if(flag){
        $('#tabs').tabs('select',title)
    }else{
        $('#tabs').tabs('add',{
            title:title,
            closable:true,//是否可以关闭
            //href:'/sales/sale_chance_index/',//跳转新的页面，样式可能会出问题
             //新增一个iframe窗口
            content:"<iframe frameborder=0 scrolling='auto' style='width:99%;height:99%' ' src='"+url+"'></iframe>",
        });
    }

}


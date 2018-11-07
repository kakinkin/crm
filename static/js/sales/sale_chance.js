// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T','')
}

//格式化状态
function formatter_state(value) {
    if ('0'==value)
        return '未分配';

    if ('1'==value)
        return '已分配';

    return value;


}


// 格式化开发状态
function  formatter_devResult(value) {
    if ('0'==value)
        return '未开发';

    if ('1'==value)
        return '开发中';

    if ('2'==value)
        return '开发完成';

    if ('3'==value)
        return '开发失败';

    return value;

}

//按条件查询营销机会
function  select_params_sale_chance() {
    //获取参数
    var customerName=$('#customerName').val().trim();
    var overview=$('#overview').val().trim();
    var createMan=$('#createMan').val().trim();
    var state=$('#state').combobox('getValue');
    //加载数据，传参查询后台
    if(customerName||overview||customerName||state)
    $('#dg').datagrid('load',{
        cn:customerName,
        ow:overview,
        cm:createMan,
        st:state

    });


}

//切换分配状态立即查询 下拉框 combobox
$("#state").combobox({
    onChange: function () {
        select_params_sale_chance();
    }
});

/**
// 初始化创建营销机会对话框
$('#sales_sale_chance_create_dialog').dialog({
   title:'添加营销机会',
    width:700,
    height:450,
    height:450,
    iconCls:'icon-add',
    resizable:false, //可调整大小
    modal:true, //模态
    draggable:false, //不可移动
    closed:true, //是否关闭
    buttons:[{
       text:'保存',
        iconCls:'icon-save',
        handler:function () {
           //先给csrf隐藏域复制
            $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

            //一打开就要，提交form表单，让后台返回查询数据
            sub_create_sale_chance_form();

        }

    },{
       text:'关闭',
        iconCls:'icon-cancel',
        handler:function () {
           $('#sales_sale_chance_create_dialog').dialog('close');

        }
    }]


});

//打开营销机会对话框
function open_sale_chance_dialog() {
    //发送ajax请求查询客户名称和联系人名称
    $.ajax({
        'type':'GET',
        'url':'customer/select_cname_and_lname_add_uname/',
        'data':{
          'csrfmiddlewaretoken':$.cookie('csrftoken')
        },
        'dataType':'json',
        'success':function (result) {
            //如果是400 显示错误信息
            if(400==result.code){
                console.log(result.msg);
            }
              // 如果是200 正常显示
            if(200==result.code){
                 // 如果数据存在则循环展示
                if (result.cs.length>0){
                    var cs = result.cs;
                    $('#customer_select').append('<option value="0">-------请选择------</option>');
                  console.log(cs);
                }
            }

        }
    })

}


//提交form表单
function sub_create_sale_chance_form() {
    $('#sales_sale_chance_form').form('submit',{
        url:'/slales/create_sale_chance/',
        success:function (result) {
            var obj=JSON.parse(result);

            //显示提示信息
            $.messager.show({
                title: '提示',
                msg:obj.msg,
                timeout:5000
            });

            //关闭对话框
            $('#sales_sale_chance_create_dialog').dialog('close');

            //如果code是200 清除对话框
            if (200==obj.code){
                $('#sales_sale_chance_form input').val('');
                $('#sales_sale_chance_form textarea').val('');
                $('#sales_sale_chance_form select').val('');
            }

        }
    });

}

*/

# -*- coding:utf-8 -*-
from django.urls import  path
from . import views

#命名空间
app_name='system'

urlpatterns=[

    #用户返回注册登录的html页面的控制函数
    path('login_register/',views.login_register,name='login_register'),
    #ajax处理是否数据库里用户名唯一
    path('system/unique_username/',views.unique_username,name='unique_username'),
    #ajax处理是否邮箱唯一可以使用
    path('system/unique_email/',views.unique_email,name='unique_email'),
    #发送邮箱验证码方法
    path('system/send_email/',views.send_email,name='send_email'),
    #处理来自激活码邮件的get请求,并返回给页面信息
    path('system/active_accounts/',views.active_accounts,name='active_accounts'),
    #处理登录
    path('system/login_user/',views.login_user,name='login_user'),
    path('index/',views.index,name='index')

]

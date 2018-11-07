# -*- coding:utf-8 -*-
from django.urls import path
from . import views
app_name='customer'
urlpatterns=[
 path('select_cname_and_lname_add_uname/',views.select_cname_and_lname_add_uname,name='select_cname_and_lname_add_uname'),

]
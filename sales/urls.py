# -*- coding:utf-8 -*-
from django.urls import path
from . import views

app_name='sales'

urlpatterns=[
    path('sale_chance_index/',views.sale_chance_index,name='sale_chance_index'),
    path('select_sale_chance_list/',views.select_sale_chance_list,name='select_sale_chance_list')

]
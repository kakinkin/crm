# -*- coding:utf-8 -*-
from _md5 import md5
from datetime import  datetime,timedelta

import base64

from django.core.paginator import Paginator

td=timedelta(minutes=10)
ts=datetime.now()+td
# print(ts,type(ts))
#<class 'datetime.datetime'>
ts=ts.timestamp()
print(ts,type(ts))


b64=base64.b64encode('张三&1234'.encode(encoding='utf-8'))
b641=b64.decode(encoding='utf-8')
#f448c0fba34ea49efe28026efd70fe23

print(b64,type(b64))
print(b641,type(b641))
password='Jia1234.'

a=md5(password.encode(encoding='utf-8')).hexdigest()
print(a,type(a))
from django.db import models
from datetime import datetime

# Create your models here.
#用户模型
class User(models.Model):
    #用户名和数据库的字段约束对应 varchar20
    username=models.CharField(max_length=20,db_column='user_name',unique=True)
    #密码，对应varchar 100
    password=models.CharField(max_length=100)
    #真实名字 varchar 20
    truename=models.CharField(max_length=20,null=True,db_column='true_name')
    #email varchar30
    email=models.CharField(max_length=30,unique=True)
    #phone varchar20
    phone=models.CharField(max_length=20,null=True)
    #是否有效int4
    is_valid=models.IntegerField(max_length=4,default=1)
    #创建时间datetime
    create_date=models.DateTimeField(default=datetime.now())
    #更新时间datetime
    update_date=models.DateTimeField(null=True)
    #随机验证码 varchar255
    code=models.CharField(max_length=255,null=True)
    #状态码是否激活tinyint
    status=models.BooleanField(max_length=1,default=0)
    #发送邮件的有效时间戳是字符串
    timestamp=models.CharField(max_length=255,null=True)

    #元信息 确保和数据表对应
    class Meta(object):
        db_table='t_user'
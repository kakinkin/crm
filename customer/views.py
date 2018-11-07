from django.shortcuts import render
from customer.models import  Customer,LinkMan
from system.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Create your views here.
# 查询客户名称和客户联系人名称和用户名称
@require_GET
def select_cname_and_lname_add_uname(request):
    try:
        #查询用户
        c=Customer.objects.values('id','name').all()

        #查询联系人
        l=LinkMan.objects.values('id','LinkName').all()

        #查询用户
        u=User.objects.values('id','username').all()

        context={
            'code':200,
            'msg':'success',
            'cs':list(c),
            'ls':list(l),
            'us':list(u)
        }

        return  JsonResponse(context)

    except ObjectDoesNotExist as e:
        print(e)
        return  JsonResponse({'code':400,'msg':'error'})





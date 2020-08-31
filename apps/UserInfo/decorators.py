from functools import wraps
from django.http import Http404
from utils import restful
from django.shortcuts import redirect

#超级管理员required装饰器
def superuser_required(viewfunc):
    @wraps(viewfunc)
    def decorator(request,*args,**kwargs):
        if request.user.is_superuser:
            return viewfunc(request,*args,*kwargs)
        else:
            raise Http404

    return decorator

#普通required装饰器
def user_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.params_error(message='请先登录！')
            else:
                return redirect('/')

    return wrapper
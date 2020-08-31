from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .form import LoginForm,SignupForm
from django.http import JsonResponse,HttpResponse
from .FormMixin import json_response
from .models import User
from utils import restful
from utils.captcha import xfz02_captcha
from django.core.cache import cache
from django.http import HttpResponse


from io import BytesIO

import utils
def loginView(request):
    form = LoginForm(request.POST)
    print('验证中')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        print('username',username)
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        print('remember',remember)
        user = authenticate(username=username, password=password)
        onlyUsername = authenticate(username=username)
        onlyUsername2 = User.objects.filter(username=username).exists()
        print('onlyUsername2',onlyUsername2)
        print(username)
        if user:
            print('user', user)
            print('帐号密码验证成功')
            if user.is_active:
                print('帐号密码激活状态')
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                    return restful.ok()
                else:
                    request.session.set_expiry(0)
                    return restful.ok()
            else:
                return restful.auth_error('帐号被冻结')
        elif onlyUsername2: #这里的username和上面的username存在冲突一次
            print('帐号存在密码错误')
            return restful.password_error('密码错误')
        else:
            return restful.account_error('帐号不存在')
    else:
        print('form.get_error()',form.get_errors())
        return restful.form_error(message=form.get_errors())


#更改密码
# def loginViews(request):
#     form = LoginForm(request.POST)
#     print('验证中')
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         print(username)
#         # remember = form.cleaned_data['remember']
#         user = User.objects.get(username=username)
#         print('user',user,user.username)
#         print('user', password,user.password)
#         user.set_password(password)
#         user.save()
#         print('验证中2')
#         authentic = authenticate(username=username,password=password)
#         print('authentic',authentic)
#         if authentic:
#             print('帐号密码验证成功')
#             if authentic.is_active:
#                 print('帐号密码激活状态')
#             else:
#                 return json_response('403','帐号被冻结')
#         else:
#             print('帐号密码验证不通过')
#             user1 = {'user':user.username}
#             return json_response('404','帐号或密码错误',user1)
#     else:
#         print('from不通过')
#         return form.get_error()

@login_required(login_url='/cms/')
def loginrequire(request):
    return HttpResponse('success')


def signupView(request):
    form = SignupForm(request.POST)
    print('signupView,1')
    if form.is_valid():
        print('signupView,2')
        username = form.cleaned_data.get('username')
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password1')
        telephone_code = form.cleaned_data.get('telephone_code')
        if telephone_code == cache.get('telephone_code') or '123456': #test
            user=User.objects.create_user(username=username,telephone=telephone,password=password,is_staff=True)
            login(request,user)
            return restful.ok()
        else:
            return restful.result(code=311,message='手机验证码错误')
    else:
        return restful.params_error(message=form.get_errors())

def logOutView(request):
    logout(request)
    return redirect('/course/index')


def img_captcha(request):
    text,image = xfz02_captcha.Captcha.gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set('code',text.lower(),2*60)
    return response


def test2(request):
    pass

def send(request):
    mobile = request.GET.get('telephone')
    codeBYweb = request.GET.get('code')
    code = cache.get('code')
    # telephone_code = cache.get('telephone_code')
    telephone_active = xfz02_captcha.Captcha.maketelephonecode()#test
    print('telephone_active',telephone_active)
    telephone_code = cache.get('telephone_code')
    print('codeBYweb', codeBYweb, 'code', code)
    if codeBYweb:
        if code == codeBYweb or '123456':
            print('OK')
            # xfz02_captcha.send_MS_to_phone(mobile=mobile)
            return restful.result(message='手机验证码为：%s'%telephone_code)
        else:
            return restful.result(code=311,message='验证码错误')
    else:
        return restful.result(code=311,message='验证码不能为空')






def index(request):
    cache.set('username','laozhu',60)
    return HttpResponse('index success!!')

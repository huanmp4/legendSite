from django.http import JsonResponse
from urllib.parse import urlencode

import json


import requests,time

class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500
    formerror = 300
    passworderror = 301
    accounterror = 302
    sendmessageerror = 311


def result(code=HttpCode.ok,message=None,data=None):
    json_dict = {'code':code,'message':message,'data':data}
    return JsonResponse(json_dict)

def params_error(message=None,data=None):
    return result(code=HttpCode.paramserror,message=message,data=data)

def auth_error(message=None,data=None):
    return result(code=HttpCode.unauth,message=message,data=data)

def password_error(message='密码错误',data=None):
    return result(code=HttpCode.passworderror,message=message,data=data)

def account_error(message='帐号不存在',data=None):

    return result(code=HttpCode.accounterror,message=message,data=data)

def method_error(message=None,data=None):
    return result(code=HttpCode.methoderror,message=message,data=data)

def server_error(message=None,data=None):
    return result(code=HttpCode.servererror,message=message,data=data)

def form_error(message=None,data=None):
    return result(code=HttpCode.formerror,message=message,data=data)

def ok():
    return result()


class FormError(object):
    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()  # {'password': [{'message': '密码长度不能少于4位', 'code': 'min_length'}]}
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return '表单无验证无数据'

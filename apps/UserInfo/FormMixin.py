from django.http import JsonResponse

class FormMixin(object):
    def get_error(self):
        if hasattr(self, 'error'):
            error = self.error.get_json_data()
            new_error = []
            for key, values in error.items(): # {'password': [{'message': '密码长度不能少于4位', 'code': 'min_length'}]}
                value_set = []
                for value in values:
                    value_set.append(value['message'])
                new_error[key] = value_set
            return new_error
        else:
            return {}

class FormMixin2(object):
    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data() # {'password': [{'message': '密码长度不能少于4位', 'code': 'min_length'}]}
            print('froms errors',errors)
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}





def json_response(code,massage=None,data=None,*args,**kwargs):
    success = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500
    print('args',args)
    print('kwargs',kwargs)
    data = {'code':code,'massage':massage,'data':data}
    if args:
        for i in args:
            data.update(i)
    if kwargs and isinstance(kwargs,dict):
        data.update(kwargs)
    return JsonResponse(data)
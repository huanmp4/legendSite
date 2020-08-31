from django import forms
from .FormMixin import FormMixin2
from .models import User

class LoginForm(forms.Form,FormMixin2):
    username = forms.CharField(max_length=11,min_length=2,error_messages={'max_length':'帐号长度不能超过11位',"min_length":"帐号长度不能少于2位",'required':'请输入帐号'})
    password = forms.CharField(max_length=11,min_length=4,error_messages={'max_length':'密码长度不能超过11位',"min_length":"密码长度不能少于4位",'required':'请输入密码'})
    remember = forms.IntegerField(required=False)

class SignupForm(forms.Form,FormMixin2):
    telephone = forms.CharField(max_length=11,min_length=11,error_messages={'max_length':'手机必须11位数','min_length':'手机必须11位数'})
    username = forms.CharField(max_length=20,min_length=2,error_messages={'max_length':'帐号机不能大于20位数','min_length':'帐号不能小于2数位'})
    password1 = forms.CharField(max_length=11,min_length=4,error_messages={'max_length':'密码长度不能超过11位',"min_length":"密码长度不能少于4位"})
    password2 = forms.CharField(max_length=11,min_length=4,error_messages={'max_length':'密码长度不能超过11位',"min_length":"密码长度不能少于4位"})
    telephone_code = forms.CharField(max_length=10)

    def clean(self):
        cleaned = super(SignupForm,self).clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')
        telephone_test = cleaned.get('telephone')
        telephone_exists = User.objects.filter(telephone=telephone_test).exists()
        if telephone_exists:
            raise forms.ValidationError('手机已被注册,如忘记密码请用手机验证码登录')
        return cleaned
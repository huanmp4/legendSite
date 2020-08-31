from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models
# class User(AbstractBaseUser,PermissionsMixin):


class UserManager(BaseUserManager):
    def _create_user(self,username,telephone,password,**kwargs):
        if not username:
            raise ValueError('请输入用户名')
        if not telephone:
            raise ValueError('请输入手机号码')
        if not password:
            raise ValueError('请输入密码')
        user = self.model(username = username,telephone = telephone ,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self,username,telephone,password,**kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = True
        return self._create_user(username,telephone,password,**kwargs)
    def create_superuser(self,username,telephone,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username,telephone,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=100,unique=True)
    telephone = models.CharField(max_length=11)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined_time = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telephone']

    objects = UserManager()

    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username
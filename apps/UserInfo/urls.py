from django.urls import path
from . import views
app_name = 'UserInfo'
urlpatterns = [
    path('loginView',views.loginView,name = 'loginView'),
    path('loginrequire',views.loginrequire,name='loginrequire'),
    path('signupView',views.signupView,name='signupView'),
    path('logoutView',views.logOutView,name='logoutView'),
    path('img_captcha/',views.img_captcha,name='img_captcha'),
    path('test2',views.test2,name='test2'),
    path('send',views.send,name='send'),
    path('index',views.index,name='index'),
]
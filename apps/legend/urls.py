from django.urls import path
from . import views
from . import views_data
from . import views_index
from . import tests
app_name = "legend"
urlpatterns = [

    path('visit',views.visit,name="visit"),
    path('check',views.check,name="check"),
    path('cleanalldata', views.CleanAllData, name="cleanalldata"),
]


#传奇发布网
urlpatterns += [
    path("getdata",views_data.getData,name="getdata"),
    path("cleanDate",views_data.cleanDate,name="cleanDate")

]

#传奇主页
urlpatterns += [
    path("",views_index.index,name="index"),

]


#测试
urlpatterns += [
    path("test",tests.test,name="test"),

]
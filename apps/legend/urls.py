from django.urls import path
from . import views
from . import views_data
from . import views_index
app_name = "legend"
urlpatterns = [
    path('test',views.index,name="test"),
    path('visit',views.visit,name="visit"),
    path('check',views.check,name="check"),
    path('cleanalldata', views.CleanAllData, name="cleanalldata"),
]


#传奇发布网
urlpatterns += [
    path("getdata",views_data.getData,name="getdata"),
    path("cleanDate",views_data.cleanDate,name="cleanDate")

]

urlpatterns += [
    path("",views_index.index,name="index"),

]
from django.test import TestCase

# Create your tests here.
from django.shortcuts import render

from django.utils import timezone
import time,datetime
from .models import legendSite

def test(request):
    a = "2013-12-11 11:00"
    legendInfo = legendSite.objects.all()
    # start = "2020-9-1 1:00"
    # end = "2020-9-11 9:00"
    # now = datetime.datetime.now()
    # today_zero = time.strftime("%Y-%m-%d 00:00:00", now.timetuple())
    # print("today_zero:",today_zero)
    # data_time = legendSite.objects.exclude(time__range=(start,end)).exclude(onPage="allDay")
    # priority2 = legendSite.objects.filter(time__range=(today_zero,today_zero))
    # for d in priority2:
    #     print(d.serverName+"time:"+time.strftime("%m-%d %H:%M",d.time.timetuple())+" "+"onPage:"+d.onPage)
    # print("database_time",time.mktime(data_time.time.timetuple()))
    # print("data1",time.mktime(datetime.datetime.now().timetuple()))
    # print("时间戳转格式时间:",time.strftime("%Y-%m-%d",time.localtime(time.mktime(data_time.time.timetuple()))))

    is_exist = legendInfo.filter(serverName="修罗酒鬼べ大极品",time=datetime.datetime.now()).exists()
    print("is_",is_exist)
    content = {"tests":a}
    return render(request,"legendCMS/test.html",content)
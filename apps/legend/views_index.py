from django.shortcuts import redirect,reverse,render
from .models import legendSite
import datetime,time

def index(request):
    legendInfo = legendSite.objects.all()
    now = datetime.datetime.now()
    tomorrow = int(time.strftime("%d",now.timetuple())) + 1 #获取明天
    minute_now = time.strftime("%M", now.timetuple())
    hour_now = int(time.strftime("%H",now.timetuple()))
    day_now = int(time.strftime("%d", now.timetuple()))
    today_zero = time.strftime("%Y-%m-%d 0:0:0", now.timetuple())  # 今天零点


    minute_start = 0 if int(minute_now) - 30 < 0 else 30
    minute_end = 59 if minute_start == 30 else 29

    minute_p3_start = 30 if int(minute_now) < 30 else 0
    minute_p3_end = 59 if minute_p3_start == 30 else 30
    hour_p3 = hour_now - 1 if minute_p3_start == 30 else hour_now

    first_start = time.strftime("%Y-%m-%d %H:" + str(minute_start) + ":0", now.timetuple())
    first_end = time.strftime("%Y-%m-%d %H:" + str(minute_end) + ":0", now.timetuple())
    third_start = time.strftime("%Y-%m-%d " + str(hour_p3)+ ":" + str(minute_p3_start) + ":0", now.timetuple()) #半小时前的服的时间
    third_end = time.strftime("%Y-%m-%d " + str(hour_p3) + ":" + str(minute_p3_end) + ":0", now.timetuple()) #半小时前的服的时间
    four_end = time.strftime("%Y-%m-" + str(day_now + 3) +" %H:%M:%S", now.timetuple())


    priority = legendInfo.filter(time__range=(today_zero, today_zero))#0点的服
    priority1 = legendInfo.filter(time__range=(first_start,first_end))#首推
    priority2 = legendInfo.filter(time__range=(today_zero, today_zero)).filter(onPage="allDay") #全日推荐服
    priority3 = legendInfo.filter(time__range=(third_start, third_end))#半小时前的服
    priority4 = ''
    if hour_now > 0 and hour_now < 7:
        priority4 = legendInfo.filter(time__range=(today_zero, today_zero)).filter(onPage="allNight")  # 通宵服
    priority5 = legendInfo.filter(time__gt = first_end)#首推之后的服

    content = {
        "legends":legendInfo,
        "priority1":priority1,
        "priority2":priority2,
        "priority3":priority3,
        "priority4":priority4,
        "priority5":priority5,

    }
    return render(request,'legendhtml/index.html',content)

#1.首推
#2.全天推荐
#3.半小时前的服
#4.首推之后的服

def searchSubmit(request):
    print('22',request.GET.get("content"))
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from .models import legendSite,oldLegendSite
import time,datetime
from utils import restful
from django.shortcuts import redirect,reverse,render
import re
from apscheduler.schedulers.blocking import BlockingScheduler

left = 0

def getData(request):
    print("开始每30分钟获取数据", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    url = "https://918hj.zjlbw.top/"
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(url)
    iframe = driver.find_elements_by_tag_name('iframe')[0]  # 查找第一个[0]iframe
    driver.switch_to.frame(iframe)  # 查找进入刚刚查找的iframe里面
    iframe = driver.find_elements_by_tag_name('iframe')[0]  # 重复
    driver.switch_to.frame(iframe)  # 重复
    soup = BeautifulSoup(driver.page_source, "html.parser")  # 解码
    soup_dl = soup.find_all("dl")
    legend_list = []
    howMany = 0
    legendInfo = legendSite.objects.all()
    for index, dl in enumerate(soup_dl):
        temp_list = []
        howMany += 1


        for a in dl.find_all("a"):
            temp_list.append(a.string)

        for b in dl.find_all("span"):
            if b.string == None or '':
                for bb in b.find_all("font"):
                    if bb.string == None or '':
                        continue
                    else:
                        temp_list.append(bb.string)
            else:
                temp_list.append(b.string)
        try:
            spanIsNone = dl.span.string
        except:
            for index,c in enumerate(dl.find_all("dd")):
                if index >= 2 and index <= 5:
                    if c.string == None or '':
                        for index,cc in enumerate(c.strings):
                            if index == 0:
                                temp_list.append(cc)
                            else:
                                continue
                        # c5 = c.parent.find(class_="c5")
                        #
                        # print("c.父节点", c.parent.find(class_="c5"))

                    else:
                        temp_list.append(c.string.replace("\xa0",""))
        temp_list.append(dl.a["href"])
        del temp_list[2]  # 把多余的删除
        legend_list.append(temp_list)

    for legend in legend_list:
        # print("dl:",legend)

        #如果时间是空的,就给个假时间给它
        if len(legend) < 4  or len(legend) >= 8:
            print("警告,列表元素小于3或大于7")
            continue
        if legend[2] == None or '':
            temp_month = time.strftime('%m', time.localtime(time.time()))
            temp_day = time.strftime('%d', time.localtime(time.time()))
            temp_legend = "%s月/%s日/★错误时间★"%(temp_month,temp_day)
        else:
            temp_legend = legend[2]
        spli = temp_legend.split("/")


        onPage = ''
        dd = ''
        if spli[0] == "---精品全天固定---":
            onPage = "allDay"
            ttime = time.strftime('%Y-%m-%d 0:0:0', time.localtime(time.time()))
            dd = ttime
            is_exist = legendInfo.filter(serverName=legend[0], time=dd).exists()
            if not is_exist:
                legendSite.objects.create(serverName=legend[0], ip=legend[1], time=dd, type=legend[3],
                                          introduce=legend[4],
                                          QQ=legend[5],href=legend[6], onPage=onPage)
        elif spli[-1] == "★通宵推荐★":
            onPage = "allNight"
            ttime = time.strftime('%Y-%m-%d 0:0:0', time.localtime(time.time()))
            dd = ttime
            is_exist = legendInfo.filter(serverName=legend[0], time=dd).exists()
            if not is_exist:
                legendSite.objects.create(serverName=legend[0], ip=legend[1], time=dd, type=legend[3],
                                          introduce=legend[4],
                                          QQ=legend[5], href=legend[6], onPage=onPage)

        elif spli[-1] == "★错误时间★":
            onPage = "error"
            ttime = time.strftime('%Y-%m-%d 0:0:0', time.localtime(time.time()))
            dd = ttime
            is_exist = legendInfo.filter(serverName=legend[0], time=dd).exists()
            if not is_exist:
                legendSite.objects.create(serverName=legend[0], ip=legend[1], time=dd, type=legend[3],
                                          introduce=legend[4],
                                          QQ=legend[5], href=legend[6], onPage=onPage)
        else:
            try:
                onPage = "normal"
                year = time.strftime('%Y', time.localtime(time.time()))
                month = spli[0].replace("月", '')
                day = spli[1].replace("日", '')
                hour = spli[2].split("点")[0]
                minute = spli[2].split("点")[1].split("开放")[0].replace('分', '')
                minute = minute if minute != '' else 0
                dd = "%s-%s-%s %s:%s:0" % (year, month, day, hour, minute)
                is_exist = legendInfo.filter(serverName=legend[0], time=dd).exists()
                if not is_exist:
                    legendSite.objects.create(serverName=legend[0], ip=legend[1], time=dd, type=legend[3],
                                              introduce=legend[4],
                                              QQ=legend[5], href=legend[6], onPage=onPage)

            except:
                onPage = "allNight"
                ttime = time.strftime('%Y-%m-%d 0:0:0', time.localtime(time.time()))
                dd = ttime
                is_exist = legendInfo.filter(serverName=legend[0], time=dd).exists()
                if not is_exist:
                    legendSite.objects.create(serverName=legend[0], ip=legend[1], time=dd, type=legend[3],
                                              introduce=legend[4],
                                              QQ=legend[5], href=legend[6], onPage=onPage)
    # return redirect(reverse('legend:check'))
    print("每30分钟获取数据执行成功",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return restful.result(code=200,message='OK')


def cleanDate():
    legendSite.objects.all().delete()


#清除1天前的私服数据
def cleanYesterdayBeforeDate():
    #把数据移动到别的表
    yesterdayData = time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()))
    oldData = legendSite.objects.filter(time__lt=yesterdayData)

    for data in oldData:
        oldLegendSite.objects.create(serverName=data.serverName, ip=data.ip, time=data.time, type=data.type,
                                              introduce=data.introduce,
                                              QQ=data.QQ, href=data.href, onPage=data.onPage)
    #删除
    legendSite.objects.filter(time__lt=yesterdayData).delete()
    print("每23小时清理数据执行成功")
    return restful.result()

def test1():
    print("每10秒运行一次",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return "表示OK"

def test2():
    print("每1分钟运行一次",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return "表示OK"

def test3():
    print("定时一分钟运行一次，共5次",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return "表示OK"

def getdata_middle():
    getData('ok')
    print("="*30)
    print("开始获取数据", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("=" * 30)

#"interval"参数是minutes,seconds,而且必须是int类型
#"cron"参数是minute,second,类型可以是str或int
def startJob(request):
    schedule = BlockingScheduler()
    # schedule.add_job(test1,"interval",minutes=1,id="test1")
    schedule.add_job(test1,"interval",seconds=10,id="test1")
    schedule.add_job(test2,"interval",minutes=1,id="test2")
    schedule.add_job(test3, "cron", hour=18, minute=16, id="test3")
    schedule.add_job(test3, "cron", hour=18, minute=17, id="test4")
    schedule.add_job(test3, "cron", hour=18, minute=18, id="test5")
    schedule.add_job(test3, "cron", hour=18, minute=19, id="test6")
    schedule.add_job(test3, "cron", hour=18, minute=20, id="test7")

    schedule.add_job(getdata_middle,"interval",minutes=1,id="getData_job")
    schedule.add_job(cleanYesterdayBeforeDate,"cron",hour=23,minute=50,id="cleanYesterdayBeforeDate_job")
    schedule.start()
    return restful.result(code=200,message='开始爬虫计划')

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from .models import legendSite
import time
from django.shortcuts import redirect,reverse,render
import re



def getData(request):
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
        print("dl:",legend)
        # spli = legend[2].split("/")
        # month = spli[0][0]
        # day = spli[1][0:2]
        # hour = spli[2][0]
        # minute = spli[2][2:4]
        # year = time.strftime('%Y', time.localtime(time.time()))
        # dd = "%s-%s-%s %s:%s:0" % (year, month, day, hour, minute)
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

    return redirect(reverse('legend:check'))

def cleanDate(request):
    legendSite.objects.all().delete()
    return redirect(reverse('legend:check'))
import os
import time
import random
import string
from PIL import Image,ImageDraw,ImageFont
from utils import restful
import requests
from django.core.cache import cache


class Captcha(object):
    font_path = os.path.join(os.path.dirname(__file__),'tt0627m_.ttf')
    number = 4
    size = (100,40)
    bgcolor = (0,0,0)
    random.seed(int(time.time()))
    font_color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
    fontsize = 23
    linecolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    draw_line = True
    draw_point = True
    line_number = 4
    source = list(string.ascii_letters)
    for num in range(0,10):
        source.append(str(num))

    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.source,cls.number))

    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([begin,end],fill = cls.linecolor)

    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100,max(0,int(point_chance)))
        for w in range(width):
            for h in range(height):
                temp = random.randint(0,100)
                if temp > 100 - chance:
                    draw.point((w,h),fill = (0,0,0))

    @classmethod
    def gene_code(cls):
        width,height = cls.size
        image = Image.new('RGBA',(width,height),cls.bgcolor) #画板
        font = ImageFont.truetype(cls.font_path,cls.fontsize) #字体路径
        draw = ImageDraw.Draw(image) #转画板为笔
        text = cls.gene_text() #获取验证码
        font_width,font_height = font.getsize(text)
        print('font_width,font_height:',font_width,font_height)
        draw.text(((width - font_width)/2, (height - font_height)/2),text=text,font=font,fill=cls.font_color)
        if cls.draw_line:
            for x in range(0,cls.line_number):
                cls.__gene_line(draw,width,height)

        if cls.draw_point:
            cls.__gene_points(draw,10,width,height)

        return (text,image)

    #makecode
    @classmethod
    def maketelephonecode(cls):
        source = '0123456789'
        code_temp = []
        for i in range(6):
            temp = random.choice(source)
            code_temp.append(temp)
        code = ''.join(code_temp)
        print('phone code:', code)
        cache.set('telephone_code', code, 60 * 2)
        return code

    # 手机发短信验证码
    @classmethod
    def send_MS_to_phone(cls,mobile):
        code = cache.get('telephone_code')
        url = 'http://v.juhe.cn/sms/send'
        params = {
            'mobile': mobile,
            'tpl_id': '200032',
            'tpl_value': '#code#=%s' % code,
            'key': 'ae3257a9897e7c2f4b79265dd6257d8c',
        }
        response = requests.get(url, params=params)
        print('response',response)
        if response['error_code'] == 0:
            return restful.ok()
        else:
            return restful.result(code=restful.HttpCode.sendmessageerror, message='手机短信发送失败')


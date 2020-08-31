from django.shortcuts import render

# Create your views here.
from django.db import models

# Create your models here.
class Array(models.Model):
    username = models.CharField(max_length=20)
    character = models.CharField(max_length=20,default='null')
    servername = models.CharField(max_length=10)
    gold = models.IntegerField()
    machine = models.CharField(max_length=50)
    ip = models.CharField(max_length=20)
    website = models.ForeignKey('WebSite',on_delete=models.SET_NULL,null=True,default='')



class allIP(models.Model):
    ip = models.CharField(max_length=20,unique=True)
    advertisement = models.ForeignKey('WebSite',on_delete=models.SET_NULL,default='',null=True)
    websitename = models.ForeignKey('WebSiteClick',on_delete=models.SET_NULL,default='',null=True)
    pub_time = models.DateTimeField(auto_now_add=True)

class WebSiteClick(models.Model):
    name = models.CharField(max_length=20,null=True,default="null")
    click = models.IntegerField()
    advertisement = models.CharField(unique=True,max_length=50,default='null')

class WebSite(models.Model):
    ip = models.CharField(max_length=20)
    advertisement = models.ForeignKey('WebSiteClick', max_length=30, on_delete=models.SET_NULL, null=True,
                                      default='null')
    content = models.CharField(max_length=20, default='null')
    country = models.CharField(max_length=10, default='null')
    province = models.CharField(max_length=10, default='null')
    city = models.CharField(max_length=10, default='null')
    isp = models.CharField(max_length=10, default='null')
    pub_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-pub_time']


class legendSite(models.Model):
    serverName = models.CharField(max_length=18)
    ip = models.CharField(max_length=18)
    time = models.DateTimeField()
    type = models.CharField(max_length=18)
    introduce = models.CharField(max_length=40)
    QQ = models.CharField(max_length=18)
    isActive = models.BooleanField(default=True)
    href = models.CharField(max_length=100,default='null')
    onPage = models.CharField(max_length=10,default="normal")
    class Meta:
        ordering = ["time"]
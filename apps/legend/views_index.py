from django.shortcuts import redirect,reverse,render
from .models import legendSite

def index(request):
    legendInfo = legendSite.objects.all()
    content = {"legends":legendInfo}
    return render(request,'legendhtml/index.html',content)
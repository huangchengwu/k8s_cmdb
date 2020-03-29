# 左侧栏连接页面

from django.shortcuts import render


from .logins import check_login
from .models import User


@check_login
def config(request):
    context = {}
    context['title'] = '配置中心'
    test1 = User(Name='huangchengwu')
    print(test1.save())
    return render(request, 'config.html', context)


@check_login
def chart(request):
    context = {}
    context['title'] = '监控'
    return render(request, 'chart.html', context)

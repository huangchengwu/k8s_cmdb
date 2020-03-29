
# 登陆模块


from django.http import HttpResponseRedirect
from django.shortcuts import render
import random
import time
from .models import User

# 退出登陆


def logout(request):
    response = HttpResponseRedirect("/")
    response.delete_cookie('k8s_cmdb_token')
    return response

# 登陆


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        print(name, password)
        # 获取数据库用户
        # 获取数据库密码

        db_user = ""
        db_pass = ""
        if name == "admin":
            if password == "admin":
                s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
                ticket = ''
                for i in range(15):
                  # 获取随机字符串
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK_' + ticket + str(now_time)
                print("--------", ticket)
                # response = HttpResponse('登陆成功')
                response = HttpResponseRedirect("/")
                # max_age 存活时间 / ticket 保存的最长时间
                response.set_cookie('k8s_cmdb_token', ticket, max_age=100000)
                # user.ticket = ticket
                # user.save()
                return response
            else:
                return render(request, 'login.html', {'imagess': '密码错误'})

        else:
            return render(request, 'login.html', {'imagess': '用户不存在'})
    else:
        return render(request, 'login.html', {'imagess': 1000})


# 检测登陆信息


def check_login(fn):
    def wrapper(request, *args, **kwargs):
        try:
            cookies = request.COOKIES['k8s_cmdb_token']
        except KeyError as err:
            print("用户不存在请登录")
            cookies = ''
        if cookies != '':
            return fn(request, *args, *kwargs)
        else:
            # 获取用户当前访问的url，并传递给/user/login/
            next = request.get_full_path()
            red = HttpResponseRedirect('/login/?next=' + next)
            return red
    return wrapper



# 第三方模块
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import git
from git import Repo
import shutil
import time
from django.core import serializers
import threading

# 自己模块
from .kubernetes import getdeployment, getnamespace, getpod, getservice
from .logins import check_login
from .forms import Create_server_froms
from .models import Create_server, exec_result_log
from .global_variable import *
import json
from .exec_server import process_cmd
# 查看k8s服务
@check_login
def show_server(request):
    context = {}
    l = {}
    if request.method == "POST":
        d = request.POST.get('selectFrom')
        if request.POST.get('selectFrom'):
            context['pod'] = getpod(d)
            context["deployment"] = getdeployment(d)
            context["service"] = getservice(d)

    context['title'] = '已部署服务'
    context['namespace'] = getnamespace()
    return render(request, 'show_server.html', context)


# 选择服务发布

@check_login
def deloy_server_select(request):
    global cache
    context = {}
    context['title'] = '发布选择'
    if request.method == "POST":
        i = 0
        for server_name in request.POST.getlist("Server_name"):
            start_time = time.strftime('%Y-%m-%d--%H:%M:%S',
                                       time.localtime(time.time()))
            shell = request.POST.getlist("shell")[i]
            t = threading.Thread(target=process_cmd, args=(
                "shell/"+shell, server_name, start_time,))
            t.start()
            print(i, "启动脚本")
            time.sleep(2)

            i += 1

        return redirect("/deloy_server/")

    get_data = request.GET.getlist("subBox")
    if request.GET.getlist("subBox"):
        if request.GET.get("deloy"):
            if get_data:

                result = []
                for n in get_data:
                    d = {}
                    repo = Repo("deloy_code/"+n)
                    print(repo.remote().pull())

                    tag_arry = []

                    data = serializers.serialize(
                        'json', Create_server.objects.filter(Server_name=n))
                    d["info"] = json.loads(data)

                    for i in repo.tags:
                        tag_arry.append(str(i))
                    if len(tag_arry) == 0:
                        print()
                        d["tag"] = [str(b) for b in repo.branches]

                    else:
                        d["tag"] = tag_arry
                    result.append(d)
                context["content"] = result
            return render(request, 'deloy_server_select.html', context)

        if request.GET.get("delete"):
            if get_data:
                for n in get_data:
                    print("---------", n)
                    shutil.rmtree("deloy_code/"+n)
                    Create_server.objects.filter(Server_name=n).delete()
                    exec_result_log.objects.filter(Server_name=n).delete()
            return redirect("/deloy_server/")
    else:
        return HttpResponse("请选择内容提交")

# 删除服务内容
@check_login
def del_server_content(request):
    get_data = request.GET.getlist("subBox")
    if get_data:
        d = {}
        for i in get_data:
            print("删除", i)

    else:
        return HttpResponse("请选择内容提交")
    return redirect("/deloy_server/")


# 发布服务页面
@check_login
def deloy_server(request):
    global cache
    context = {}
    context['title'] = '发布服务'
    context['content'] = Create_server.objects.all()
    exec_result_log_all = exec_result_log.objects.all()

    context['deloy_server_info'] = exec_result_log_all
    if request.method == "POST":
        deloy_server_info_arry = []
        if cache:
            for k, v in cache.items():
                if v["Status"] == "进行中":
                    deloy_server_info_arry.append(v)

        d = {
            "result": deloy_server_info_arry
        }
        return HttpResponse(json.dumps(d))
    return render(request, 'deloy_server.html', context)


# 执行结果
@check_login
def show_exec_result(request):
    context = {}
    result = {}
    context['title'] = '执行结果'
    context['result'] = exec_result_log.objects.get(
        Start_time=request.GET.get("Start_time"))

    return render(request, 'show_exec_result.html', context)


# 执行过程
@check_login
def show_exec_process(request):
    global cache
    context = {}
    result = {}

    if request.method == "POST":
        d = {}
        body = json.loads(request.body.decode())
        try:
            d = cache[body["Start_time"]]

        except KeyError as err:
            print("执行查询不存在", err)
            return HttpResponse(json.dumps({"stdout": "查询不存在"}))

        return HttpResponse(json.dumps(d))

    context['title'] = '执行过程'
    start_time = request.GET.get("Start_time")
    server_name = request.GET.get("Server_name")
    context["result"] = cache[start_time]

    return render(request, 'show_exec_process.html', context)


# 创建服务
@check_login
def create_server(request):
    context = {}
    create_server_froms = Create_server_froms
    context['title'] = '创建服务'
    if request.method == "POST":

        submit_from = Create_server_froms(request.POST)
        print("表单验证", submit_from.is_valid())
        if submit_from.is_valid():

            soup = BeautifulSoup(str(submit_from), 'lxml')
            server_name = soup.find(
                "input", {"name": "Server_name"})["value"]
            git_url = soup.find(
                "input", {"name": "Git_url"})["value"]
            print("创建服务", git_url, "deloy_code/"+server_name+"/")

            try:

                Repo.clone_from(
                    url=git_url, to_path="deloy_code/"+server_name+"/")

            except git.GitCommandError as err:

                print(err)

            submit_from.save()

            return redirect("/deloy_server/")
        else:
            return HttpResponse("创建服务失败")

    return render(request, 'create_server.html', {'create_server_froms': create_server_froms}, context)

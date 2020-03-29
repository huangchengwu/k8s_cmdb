# 执行模块  包括jenkins  ansible  所有执行引擎
# 执行命令实时存到缓存
import subprocess
from .global_variable import *
import time

from .models import exec_result_log


def process_cmd(args_list, server_name, start_time):
    global cache
    cache[start_time] = {
        "Status": "进行中",
        "Stdout": "",
        "Exec": args_list,
        "End_time": "",
        "Server_name": server_name,
        "Start_time": start_time
    }
    print("执行", args_list, server_name, start_time)

    popen = subprocess.Popen(args_list, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    i = 0
    while True:
        line = popen.stdout.readline()
        if not line:

            end_time = time.strftime('%Y-%m-%d--%H:%M:%S',
                                     time.localtime(time.time()))
            insert = exec_result_log(Start_time=start_time, Status='执行完毕', Exec=args_list,
                                     Server_name=server_name, Stdout=cache[start_time]["Stdout"], End_time=end_time)
            insert.save()
            cache[start_time]["Status"] = "执行完毕"
            del cache[start_time]

            break

        print("进度", i, line)
        i += 1
        cache[start_time]["Stdout"] += line.decode()
        print("缓存", cache)

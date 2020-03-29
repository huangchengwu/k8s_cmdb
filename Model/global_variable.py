# 全局变量
import requests


# 定义执行过程缓存
cache = {}


# 请求超时重试次数

requests.adapters.DEFAULT_RETRIES = 5

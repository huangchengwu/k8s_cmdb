
# Create your models here.


from django.db import models


# 用户账号密码
class User(models.Model):
    # 用户名
    Name = models.CharField(max_length=20)
    # 密码
    Password = models.CharField(max_length=255)
    # token
    Ticket = models.CharField(max_length=20)

    class Meta:
        db_table = 'userinfo'


class Create_server(models.Model):

    ID = models.AutoField(primary_key=True)
    # 服务名
    Server_name = models.CharField(
        max_length=255, unique=True)
    # 描述
    Describe = models.TextField()
    # git地址
    Git_url = models.CharField(
        max_length=255)
    # shell
    Shell = models.CharField(max_length=255)
    # 项目类型
    ProjectType = models.CharField(max_length=255)
    # 钉钉地址
    Ding = models.CharField(max_length=202)

    class Meta:
        verbose_name = "服务名"
        verbose_name_plural = verbose_name
        db_table = 'create_server'


class exec_result_log(models.Model):
    Id = models.AutoField(primary_key=True)
    # 启动时间
    Start_time = models.CharField(max_length=255)
    # 结束时间
    End_time = models.CharField(max_length=255)
    # 状态
    Status = models.CharField(max_length=255)
    # 执行脚本
    Exec = models.CharField(max_length=255)
    # 输出内容
    Stdout = models.TextField()
    # 执行服务名
    Server_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'exec_result_log'

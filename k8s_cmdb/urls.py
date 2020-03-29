
from django.urls import path
from django.conf.urls import url
from Model import services
from Model import logins
from Model import views

urlpatterns = [

    url(r'^$',  views.config, name="config"),
    url(r'^chart/', views.chart, name="chart"),

    url(r'^login/', logins.login, name='login'),
    url(r'^logout/', logins.logout, name='logout'),

    url(r'^show_server/', services.show_server, name="show_server"),
    url(r'^deloy_server/', services.deloy_server, name='deloy_server'),
    url(r'^create_server/', services.create_server, name='create_server'),
    url(r'^deloy_server_select/', services.deloy_server_select, name='select_content'),
    url(r'^show_exec_result/', services.show_exec_result, name='show_exec_result'),
    url(r'^show_exec_process/', services.show_exec_process, name='show_exec_process')

]

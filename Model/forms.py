from django import forms
from django.forms import widgets
from .models import Create_server


class Create_server_froms(forms.ModelForm):
    class Meta:
        model = Create_server

        fields = '__all__'

        widgets = {
            'Server_name': forms.widgets.TextInput(attrs={'class': 'form-control is-valid', "placeholder": "发布名字用于查看"}),
            'Describe': forms.widgets.Textarea(attrs={'class': 'form-control is-valid', "placeholder": "描述"}),
            'Git_url': forms.widgets.TextInput(attrs={'class': 'form-control is-valid', "placeholder": "git地址"}),
            'Shell': forms.widgets.TextInput(attrs={'class': 'form-control is-valid', "placeholder": "shell路径"}),
            'ProjectType': forms.widgets.TextInput(attrs={'class': 'form-control is-valid', "placeholder": "项目类型例如java"}),
            'Ding': forms.widgets.TextInput(attrs={'class': 'form-control is-valid', "placeholder": "钉钉token地址"}),

        }

        labels = {
            'server_name': '服务名',
            'describe': '描述',
            'git_url': 'git地址',
            'shell': 'shell名字',
            'projectType': '项目类型',
            'Ding': '钉钉token'
        }

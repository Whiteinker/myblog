# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 0:15
# @Author  : LiChao

from django import forms
from king import models
from django.forms import ModelForm
from django.forms.fields import CharField

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


# class MyUser(ModelForm):
#     def __new__(cls, *args, **kwargs):
#         for field_name,field_obj in cls.base_fields.items():
#             # print(field_name,dir(field_obj))
#             # print('field_name', field_name)
#             # print('field_obj', field_obj)
#             field_obj.widget.attrs['class'] = 'form-control'
#
#
#         return ModelForm.__new__(cls)
#     class Meta:
#         model = models.MyUser
#         fields =['email','password',]

class ArticleForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            print(field_name,field_obj.label)
            # print('field_name', field_name)
            # print('**kwargs', field_obj)
            no_display_title = [ 'content']
            no_display_html = ['title_image','content']
            if field_name in no_display_html:
                field_obj.widget.attrs['style'] = 'display:none;'
            if field_name in no_display_title:
                field_obj.label = ''
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)
    class Meta:
        model = models.Artical
        fields='__all__'
        # exclude = ("content",'title_image')


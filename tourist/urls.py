# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 18:00
# @Author  : LiChao

from django.conf.urls import url

from tourist import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^test$',views.test),
    url(r'^index$',views.index),
    url(r'^search/(?P<tag_id>\w+)',views.tag_search,name='search'),
    url(r'get_comment',views.get_comment,name='get_comment'),


    url(r"^(?P<category>\w+)/(?P<plate>\w+)/(?P<id>\d+)",views.artical,name='artical'),
    url(r"^(?P<category>\w+)/(?P<plate>\w+)",views.artical_list,name='artical_list'),
    url(r"^(?P<plate>\w+)/",views.plate,name='plate'),
]

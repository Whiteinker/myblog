# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 17:37
# @Author  : LiChao

from django.conf.urls import  url

from king import views

urlpatterns = [
    url(r'^$',views.admin_index,name="lc"),
    url(r'^login/$',views.acc_login,name="login"),
    url(r'^logout/$',views.acc_logout,name="logout"),
    # url(r'^index/$',views.admin_index),
    url(r'^upload',views.upload,name='upload_image'),
    url(r'^uoload_title_image', views.uoload_title_image, name='upload_title_image'),
    url(r'^artical/add$',views.write,name='writepage'),  #新添加页面
    url(r'^createuser$',views.create_user,name='createuser'),

    url(r'^artical/(?P<id>\d+)$',views.edit_art,name="editepage"),
    url(r'^(?P<table>\w+)/$',views.table,name="table_list"),
    url(r'^(?P<table>\w+)/add$',views.add,name='add'),
    url(r'^(?P<table>\w+)/(?P<id>\w+)/delete$',views.delete,name='delete'),
    url(r'^(?P<table>\w+)/(?P<id>\d+)$',views.edit),




    # url(r'^table_list',views.table_list,name="artical_list"),
    # url(r'^admin_index',views.admin_index,name='admin_inde')


# (r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',

]

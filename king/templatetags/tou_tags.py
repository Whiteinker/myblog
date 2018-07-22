# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 21:54
# @Author  : LiChao
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import  datetime,timedelta
import re
import king.models
from django.core.exceptions import FieldDoesNotExist

from king import models

register = template.Library()

@register.simple_tag
def navigation(path):
    # print('tou_tag',path)
    path = path.strip()
    path = path.strip('/')
    if path == '':
        return ''

    path_list = path.split('/')
    if len(path_list) == 2:
        category = models.Category.objects.get(url='/'+path).name
        return  mark_safe('''<li class="active">{}</li>''').format(category)
    else:
        category=models.Category.objects.get(url='/'+path_list[0]+'/'+path_list[1]).name
        category_id = models.Category.objects.get(url='/'+path_list[0]+'/'+path_list[1]).id
        plate=models.Plate.objects.get(url="/"+path).name
        return mark_safe('''<li><a href="{}?c_f={}">{}</a></li><li class="active">{}</li>''').format('/'+path_list[0]+'/'+path_list[1],category_id,category,plate)


# PAGE_ITEM_NUM = 2
# from tourist.tour_func import *
# @register.simple_tag
# def build_page_item(url_dict,artical):
#     print('tou_tags',artical)
#     page_item_obj =  buildpage(PAGE_ITEM_NUM,artical)
#     print('tou_tag_',page_item_obj.get_page_item(1))
#     return page_item_obj.get_page_item(1)
import time
@register.simple_tag
def mcache():
    now_time = time.time()
    return now_time
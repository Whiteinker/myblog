# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 21:54
# @Author  : LiChao
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import  datetime,timedelta

import king.models
from django.core.exceptions import FieldDoesNotExist

from king import models

register = template.Library()

@register.simple_tag
def display_content(id):
    content = models.Artical.objects.get(id=id).content
    content = content.replace("'","\\'")
    return mark_safe(content)
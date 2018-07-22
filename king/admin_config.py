# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 16:06
# @Author  : LiChao
from django.forms import ModelForm
from king import models
enable_admins = {}




class BaseAdmin(object):
    list_display = []
    # list_filters = []           #过滤
    # list_per_page = 20          #每一页显示的条目
    # search_fields = []          #可根据xx查找的字段
    # ordering = None             #默认排序字段，
    # filter_horizontal = []      #复选框
    # actions = ["delete_selected_objs"]
    # readonly_table = False
    # readonly_fields = ()
    # modelform_excule_fields = ()

class Category(BaseAdmin):
    list_display = "__all__"

class Plate(BaseAdmin):
    list_display = "__all__"

class Artical(BaseAdmin):
    pass
    # list_display = "__all__"


class Artical_tag(BaseAdmin):
    list_display = "__all__"
class Myuser(BaseAdmin):
    list_display = ['email','username']

def register(model_class,admin_class=None):
    if model_class not in enable_admins:
        enable_admins[model_class._meta.model_name] = admin_class
    admin_class.model = model_class



register(models.Category,Category)
register(models.Plate,Plate)
register(models.Artical,Artical)
register(models.Artical_tag,Artical_tag)
register(models.MyUser,Myuser)

# print('er',enable_admins)





def create_model_form(table,instance=None):
    '''动态生成MdoeForm'''
    model_  = enable_admins[table].model
    admin_class = enable_admins[table]
    print('create_models_form',admin_class().list_display)
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            # print(field_name,field_obj.label)
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model = model_
        fields = admin_class().list_display

    attrs = {'Meta':Meta,}
    _model_form_class = type("DynamicModelForm", (ModelForm,),attrs)
    setattr(_model_form_class,'__new__',__new__)
    return _model_form_class
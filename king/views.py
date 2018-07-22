import json
import re

import redis
from django.forms import modelformset_factory


from king import forms
import datetime
import random
import os
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.mail import send_mail

from king import models
from Myblog import settings
from king import admin_config

from king.function_ import *
# Create your views here.




@login_required(login_url='/lc/login/')
@is_admin()
def admin_index(request):
    userinfo = get_userinfo(request)

    display_table = admin_config.enable_admins
    # print(display_table)
    return render(request,'admin_index.html',{"userinfo":userinfo,
                                              "display_table":display_table,
                                              })
@login_required(login_url='/lc/login/')
@is_admin()
def table(request,table):
    userinfo = get_userinfo(request)
    admin_class = admin_config.enable_admins[table].model
    obj_list = admin_class.objects.all()
    return render(request, 'table_list.html', {"obj_list":obj_list,
                                        "userinfo":userinfo,
                                        "table":table})
@login_required(login_url='/lc/login/')
@is_admin()
def edit(request,table,id):
    userinfo = get_userinfo(request)
    model_class = admin_config.enable_admins[table].model
    model_form = admin_config.create_model_form(table)
    obj = model_class.objects.get(id=id)
    from_obj = model_form(instance=obj)
    if request.method == "POST":
        # print('asdf')
        from_obj = model_form(request.POST,instance=obj)
        from_obj.save()
    return render(request, 'edit.html', {"from_obj":from_obj,
                                        "userinfo":userinfo,
                                        "table":table,
                                        "id":id,
                                         })
@login_required(login_url='/lc/login/')
@is_admin()
def add(request,table):
    userinfo = get_userinfo(request)
    admin_class = admin_config.enable_admins[table].model
    model_form = admin_config.create_model_form(table)
    from_obj = model_form()
    if request.method == "POST":
        print(request.POST)
        from_obj = model_form(request.POST)
        from_obj.save()
        return redirect("/lc/{}".format(table))
    return render(request, 'edit.html', {"from_obj":from_obj,
                                        "userinfo":userinfo,
                                        "table":table,
                                         })
@login_required(login_url='/lc/login/')
@is_admin()
def delete(request,table,id):
    userinfo = get_userinfo(request)
    if request.method == "POST":
        admin_class = admin_config.enable_admins[table].model
        print('admin_class',admin_class)
        admin_class.objects.get(id=id).delete()
        # print('aaa',request.POST.get("_id"))
    return redirect("/lc/{}".format(table))


def acc_login(request):
    # print('iiin', request.GET.get('next'))
    next_url = request.GET.get('next')
    if request.method == "POST":
        _email = request.POST.get("email")
        _password = request.POST.get("password")
        user = auth.authenticate(username=_email, password=_password)
        if user:
            auth.login(request,user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')
    if next_url:
        return render(request,'login.html',{"next_url":next_url})
    else:
        return render(request, 'login.html')

from django.utils.safestring import mark_safe
def create_user(request):
    print('yes')
    host_name = request.META['HTTP_HOST']
    '''在登陆页面，创建新用户 ,'''
    rec_data = dict()
    if request.is_ajax():    #sign(0：表示只有邮箱,要求发送验证码，1：表示验证码邮箱和密码)
        if request.POST.get('sign') == '0':

            ttl = get_get_valid_num_ttl(host_name)
            if ttl == None:
                set_get_valid_num_ttl(host_name)   #设置同一个ip 获取验证码的间隔时长

                client_ip = request.META.get('REMOTE_ADDR')
                email = request.POST.get('email')
                if valid_email1(email):     #验证是否是邮箱
                    sendmail_sucess = send_valid_num(email,host_name)     #发送验证码，并保存至redis
                    print('邮件发送成功??',sendmail_sucess)
                    # sendmail_sucess = True
                    # if not sendmail_sucess:
                    #     rec_data['msg'] = '发送失败,请确认您的邮箱是否正确'
                    # else:
                    rec_data['ttl'] = GET_VALID_NUM_TIME
                    rec_data['msg'] = '验证码已发送,十分钟内有效，请及时查阅您的邮件'
                else:
                    rec_data['msg'] = '请输入正确的邮箱'
                    rec_data['ttl'] = '0'
            else:
                rec_data['ttl'] =ttl
                rec_data['msg'] = '验证码已发送，十分钟内有效，请及时查阅您的邮件'
        if request.POST.get('sign') == '1':
            print('sign',1)
            valid_num = request.POST.get('valid_num')
            email = request.POST.get('email')
            passwd = request.POST.get('passwd')
            passwd_ = request.POST.get('passwd_')

            # print('e',email)
            # print('v',valid_num)
            valid_num_staus =  get_valid_num(email,valid_num)

            if not valid_num_staus['code']:    #判断验证码是否过期或者错误   return{"code":"","msg":"{}"}
                rec_data.update(valid_num_staus['msg'])
                # print(1)
            elif not passwd != passwd_:
                # print(2)
                rec_data['passwd_msg'] = '两次密码不相同'
            elif len(passwd) < 3:
                # print(3)
                rec_data['passwd_msg'] = '密码至少3位'
            else:
                print(4)
                try:
                    if models.MyUser.objects.get(email=email):
                            models.MyUser.objects.get(email=email).delete()
                except Exception as e:
                    print(e)

                rec_data['passwd_msg'] = '注册/修改密码成功,请重新登陆'
                print("rec_data:",rec_data)
                models.MyUser.objects.create_user(email,passwd)

        rec_data = json.dumps(rec_data)
        print("rec_data",rec_data)
        return HttpResponse(rec_data)


def acc_logout(request):
    auth.logout(request)
    print('oout',request.GET.get('next'))
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect('/')



@login_required(login_url='/lc/login/')
@is_admin()
def edit_art(request,id):
    '''博客文章编辑页面'''
    userinfo = get_userinfo(request)
    obj = models.Artical.objects.get(id=id)
    if request.method == 'POST':
        f = forms.ArticleForm(request.POST,instance=obj)
        if f.is_valid():
            f.save()
    formset = forms.ArticleForm(instance=obj)
    return render(request,'write.html',{
                                        "formset":formset,
                                        "userinfo":userinfo,
                                        'id':id,
                                        'obj':obj,

                                        })
@login_required(login_url='/lc/login/')
@is_admin()
def write(request):
    '''博客添加页面'''
    userinfo = get_userinfo(request)
    if request.method == 'POST':
        f = forms.ArticleForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect("/lc/artical")
    formset = forms.ArticleForm()
    return render(request,'write.html',{
                                        "formset":formset,
                                        "userinfo":userinfo,
                                        })




@login_required(login_url='/lc/login/')
@is_admin()
def uoload_title_image(request):
    '''标题图片上传'''
    if request.is_ajax():
        salt = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        local_path = settings.TITLE_IMAGE          #本地路径
        res = {"code": 200, "src":""}
        relative_path = datetime.datetime.now().strftime("%Y/%m/%d/")      #图片在该项目中目录
        try:
            fpath = local_path+relative_path              #本地图片父路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            for k, file_obj in request.FILES.items():
                img_name = file_obj.name
                while True:
                    if os.path.exists(fpath+img_name):
                        img_name = ''.join(random.sample(salt, 8)) + ".jpg"
                    else:
                        break
                with open(local_path + relative_path + img_name, "wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
                res['src'] = settings.IMAGE_URL + relative_path + img_name
                # res['src']="http://"+host_name+settings.IMAGE_URL+relative_path+img_name
        except:
            res["code"] = 0
            res['msg'] = '服务器保存文件出错，请刷新页面重新上传'
        res = json.dumps(res)
        print(res)
        return HttpResponse(res)

@login_required(login_url='/lc/login/')
@is_admin()
def upload(request):
    '''富文本编辑器上传图片'''
    '''        for k, file_obj in request.FILES.items():
            with open('E:/a.jpg', "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)'''
    if request.method == 'POST':
        salt = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        local_path = settings.IMAGE
        res = {"errno":0, "data": []}
        relative_path = datetime.datetime.now().strftime("%Y/%m/%d/")
        try:
            fpath = local_path+relative_path
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            for k, file_obj in request.FILES.items():
                print('image:',k,'image_name',file_obj.name)
                img_name = file_obj.name
                while True:
                    if os.path.exists(fpath+img_name):
                        img_name = ''.join(random.sample(salt, 8)) + ".jpg"
                    else:
                        break
                with open(local_path + relative_path + img_name, "wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
                res['data'].append(settings.IMAGE_URL+relative_path+img_name)
        except:
            res['errno'] = '服务器保存文件出错，请重新上传'

        res = json.dumps(res)
        return HttpResponse(res)


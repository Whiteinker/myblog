# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 20:46
# @Author  : LiChao
from django.http import HttpResponse
from king import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def is_admin(*fargs,**fkwargs):
    def f1(out_fun):
        def rec_para(request,*args,**kwargs):
            if not request.user.id:
                return HttpResponse('<h1> Permission denied;</h1>')
            if not models.MyUser.objects.get(id=request.user.id).is_admin:
                return HttpResponse('<h1>Permission denied;</h1>')
            return out_fun(request,*args,**kwargs)
        return rec_para
    return f1



def get_userinfo(request):   #获取登录用户信息，用户发送给前端
    userinfo = None
    if request.user.id != None:
        return models.MyUser.objects.get(id=request.user.id)

def valid_email1( email ):      #用于检测用户发过来的邮箱是否合法
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


from django.core.mail import send_mail
import random
from Myblog import settings
import redis




GET_VALID_NUM_TIME = 30  #验证码发送间隔时长
VALID_TTL = 600

def send_valid_num(email,host_name):

    try:
        salt = "1234567890"
        valid_num = ''.join(random.sample(salt, 4))
        # html = '''您的验证码是{}<br>十分钟内有效<br><a href='http://{}'>点击打开网站</a>'''.format(valid_num, host_name)
        send_mail('验证码', '''您的验证码是{}\n十分钟内有效,\n来自http://{}'''.format(valid_num, host_name),
                  settings.DEFAULT_FROM_EMAIL,[email,], fail_silently=False)
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        r.setex(email,valid_num,VALID_TTL)
        return True
    except Exception as e:
        print('发送邮件错误:',e)
        return False

def get_valid_num(email=None,valid_num=None):
    rec_data = {'code':False}
    if valid_num != '' and valid_num != None:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        redis_valid_num = r.get(email)
        if redis_valid_num != None:
            redis_valid_num = redis_valid_num.decode()
            if redis_valid_num != valid_num:
                rec_data['msg'] = {}
                rec_data['msg']['valid_msg'] = '验证码错误'
            else:
                rec_data['code'] = True
                # r.delete(email)
        else:
            rec_data['msg'] = {}
            rec_data['msg']['valid_msg'] = '请获取验证码'
    else:
        rec_data['msg'] = {}
        rec_data['msg']['valid_msg'] = '请输入验证码'

    return rec_data



def set_get_valid_num_ttl(client_ip):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.setex(client_ip,'', GET_VALID_NUM_TIME)

def get_get_valid_num_ttl(client_ip):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    ttl = r.ttl(client_ip)
    if ttl != None:
        return ttl
    else:
        return None

# def get_comment(parent_comment_obj):
#     comm_dict = dict()  #{}
#     for obj in parent_comment_obj:
#         comm_dict[obj.user.email] = {}
#         comm_dict[obj.user.email]['comment'] = obj.content
#         child = obj.comment.filter(parent=obj)
#         if child:      #如果有子评论
#             comm_dict[obj.user.email]['children'] = get_comment(obj.comment.all())
#     return comm_dict
import json

from django.shortcuts import render, redirect,HttpResponse

# Create your views here.
from king import models
from django.utils.safestring import mark_safe
import time
# from django.views.decorators.cache import cache_page
from tourist.tour_func import *
# @cache_page(60*1)
def index(request):
    ttime = time.time()
    path='/'
    urldict = request.GET
    userinfo = None
    if request.user.id !=None:
        userinfo = models.MyUser.objects.get(id=request.user.id)
    categorys = models.Category.objects.all()
    artical_all = models.Artical.objects.all().order_by('title')
    tag = models.Artical_tag.objects.all()

    artical_build_page = buildpage(5, artical_all)    #（每页放的item数量）
    if not request.GET.get('page'):
        artical = artical_build_page.get_page_item()
    else:
        artical = artical_build_page.get_page_item(request.GET.get('page'))
    buildpage_ = artical_build_page.get_a_display(path,urldict)
    return render(request,'tourist/index.html', {"categorys": categorys,
                                                 'tags':tag,
                                                 "artical":artical,
                                                 "path":path,
                                                 "userinfo":userinfo,
                                                 'url_dict':urldict,
                                                 'buildpage_':buildpage_,
                                                 'ttime':ttime,
                                                 })
#根据类型查询
def plate(request,plate):  #显示plate
    urldict = request.GET
    if request.GET.get('c_f'):
        category_id = request.GET.get('c_f')
    else:
        return redirect('/')
    userinfo = None
    if request.user.id != None:
        userinfo = models.MyUser.objects.get(id=request.user.id)
    path = request.path
    categorys = models.Category.objects.all()
    tags = models.Artical_tag.objects.all()
    artical_all = models.Artical.objects.filter(plate=models.Category.objects.get(id=category_id).plate.all())

    artical_build_page = buildpage(5, artical_all)
    if not request.GET.get('page'):
        artical = artical_build_page.get_page_item()
    else:
        artical = artical_build_page.get_page_item(request.GET.get('page'))
    # buildpage_=''
    buildpage_ = artical_build_page.get_a_display(path, urldict)

    return render(request, 'tourist/index.html', {"categorys": categorys,
                                                  "artical": artical,
                                                  "tags":tags,
                                                  "path":path,
                                                  "userinfo": userinfo,
                                                  'buildpage_': buildpage_,
                                                  })
#根据版块查询
def artical_list(request,category,plate):
    urldict = request.GET
    if request.GET.get('p_f'):
        plate_id = request.GET.get('p_f')
    else:
        return redirect('/')

    userinfo = None
    if request.user.id != None:
        userinfo = models.MyUser.objects.get(id=request.user.id)
    path = request.path
    categorys = models.Category.objects.all()
    tags = models.Artical_tag.objects.all()
    artical_all = models.Artical.objects.all().order_by('title').filter(plate=plate_id)

    artical_build_page = buildpage(5, artical_all)
    if not request.GET.get('page'):
        artical = artical_build_page.get_page_item()
    else:
        artical = artical_build_page.get_page_item(request.GET.get('page'))
    # buildpage_=''
    buildpage_ = artical_build_page.get_a_display(path, urldict)
    return render(request, 'tourist/index.html', {"categorys": categorys,
                                                  "artical": artical,
                                                  "path":path,
                                                  "tags":tags,
                                                  "userinfo": userinfo,
                                                  'buildpage_': buildpage_,
                                                  })

def tag_search(request,tag_id):
    '''用标签查询'''
    userinfo = None
    if request.user.id != None:
        userinfo = models.MyUser.objects.get(id=request.user.id)
    tags = models.Artical_tag.objects.all()
    t = models.Artical_tag.objects.get(id=tag_id)
    artical_all = models.Artical.objects.filter(tags=t).distinct()

    path = request.path
    urldict = request.GET
    artical_build_page = buildpage(5, artical_all)
    if not request.GET.get('page'):
        artical = artical_build_page.get_page_item()
    else:
        artical = artical_build_page.get_page_item(request.GET.get('page'))

    buildpage_ = artical_build_page.get_a_display(path, urldict)
    return render(request, 'tourist/index.html', {"artical":artical,
                                                  "userinfo":userinfo,
                                                  "tags":tags,
                                                  "path":'/',
                                                  "buildpage_":buildpage_,
                                                  })


def artical(request,category,plate,id):
    '''显示文章'''
    userinfo = None
    if request.user.id != None:
        userinfo = models.MyUser.objects.get(id=request.user.id)
    path = 'pub'+'/'+category+'/'+plate
    content = mark_safe((models.Artical.objects.get(id=id).content))


    return render(request, 'tourist/artical.html', {
                                                "id":id,
                                                "path": path,
                                                "content":content,

                                                "userinfo": userinfo,
                                                  })
def test(request):
    # print(request.is_ajax())
    # if request.is_ajax():
    #     print(request.FILES)
    #     # for k, file_obj in request.FILES.items():
    #     #     with open('E:/a.jpg', "wb") as f:
    #     #         for chunk in file_obj.chunks():
    #     #            f.write(chunk)
    #     #
    #     # res = {"code":200,"src":"http://127.0.0.1:8000/media/1.jpg"}
    #     # res = json.dumps(res)
    #     # return HttpResponse(res)
    # if request.method == "POST":
    #     print('sssss')
    return render(request,'tourist/doc.html')


def get_comment(request):
    if request.is_ajax():
        art_id = request.POST.get('art_id')
        parent_comment_obj = models.Artical.objects.get(id=art_id).comment_set.filter(parent=None)
        comment_ = get_all_comment(parent_comment_obj)
        comment = json.dumps(comment_)
        return HttpResponse(comment)
    else:
        return HttpResponse("What are you doing?")

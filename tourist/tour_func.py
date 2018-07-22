# -*- coding: utf-8 -*-
# @Time    : 2018/4/30 18:04
# @Author  : LiChao
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
class buildpage:
    def __init__(self,num,item=[]):   #每一页放的数量，和item总量
        self.num = num
        if num<len(item):
            self.num=len(item)
        self.item =Paginator(item, num)
    def get_page_item(self,page_num=1):
        page=self.item.page(page_num)
        print(page.object_list)
        return page.object_list
    def get_a_display(self,path,urldict,n=5,):
        '''path是页面的url路径,urldict是页面携带的参数(djang.http.querydict形式，包含请求的page），n 表示分页界面可显示的页码个数（底部分页a标签数量）
        思路：判断总页数self.item.num_pages是否足够n(默认为5)页,不足显示self.item.num_pages页数
        足够则判断是
        前五页，...
        中间的...
        最后5页...'''
        page_num=1    #默认为1
        urldict = urldict.copy()
        if urldict.get('page'):
            page_num = int(urldict.get('page'))
            urldict.pop('page')

        url= path + '?' + urldict.urlencode()+'&page={}'
        # 首页
        first = '''<nav aria-label="Page navigation"> 
					<ul class="pagination">
						<li >
							<a href="{href}">
								<span aria-hidden="true">首页</span>
							</a>
						</li>'''.format(href=url.format(str(1)))
        page = '''<li {item}><a  href="{href}">{num}</a></li>'''
        # 最后一页
        last = '''  <li >
							<a href="{href}" aria-label="Next">
								<span aria-hidden="true">尾页</span>
							</a>
						</li>
					</ul>
				</nav>'''.format(href=url.format(str(self.item.num_pages)))
        def build_body(start,end):
            '''根据需要的首页和尾页生成html'''
            html = ''
            for i in range(start, end):
                if i != page_num:
                    html += page.format(href=url.format(str(i)), num=str(i), item='')
                else:
                    html += page.format(href=url.format(str(i)), num=str(i), item='class="active"')
            return first+html+last
        if self.item.num_pages < n:
            html = build_body(1,self.item.num_pages+1)
            return mark_safe(html)
        elif page_num <= self.item.num_pages and page_num > 0 :
            if page_num < n-1 :
                html = build_body(1, n+1)
                return mark_safe(html)
            if page_num > self.item.num_pages-n+2:
                html = build_body(self.item.num_pages-n+1,self.item.num_pages+1)
                return mark_safe(html)
            else:
                html = build_body(page_num-n//2,page_num+n//2+1)
                return mark_safe(html)

def get_all_comment(parent_comment_obj):
    comm_dict = dict()  #{}
    for obj in parent_comment_obj:
        comm_dict[obj.user.email] = {}
        comm_dict[obj.user.email]['comment'] = obj.content
        child = obj.comment.filter(parent=obj)
        if child:      #如果有子评论
            comm_dict[obj.user.email]['children'] = get_all_comment(obj.comment.all())
    return comm_dict
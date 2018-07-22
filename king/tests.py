from django.test import TestCase
from king import models
# Create your tests here.
def get_upload_to():
    print("___________",)
    return 'a'




artical_id = 3
parent_comment_obj = models.Artical.objects.get(id=artical_id).comment_set.filter(parent=None)
def get_comment(parent_comment_obj):
    comm_dict = dict()  #{}
    for obj in parent_comment_obj:
        comm_dict[obj.user.email] = {}
        comm_dict[obj.user.email]['comment'] = obj.content
        child = obj.comment.filter(parent=obj)
        if child:      #如果有子评论
            comm_dict[obj.user.email]['children'] = get_comment(obj.comment.all())
    return comm_dict

comm = get_comment(parent_comment_obj)
print(comm)


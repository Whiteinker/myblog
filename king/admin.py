from django.contrib import admin

# Register your models here.
from king import models
@admin.register(models.MyUser)
class User(admin.ModelAdmin):
    pass

class Category(admin.ModelAdmin):
    list_filter = ['name',]


class Plate(admin.ModelAdmin):
    pass

class Artical_tag(admin.ModelAdmin):
    pass

class Artical(admin.ModelAdmin):
    list_filter = ['title',]

class Comment(admin.ModelAdmin):
    pass

@admin.register(models.Artical_image)
class artical_img(admin.ModelAdmin):
    pass

admin.site.register(models.Category,Category)
admin.site.register(models.Plate,Plate)
admin.site.register(models.Artical_tag,Artical_tag)
admin.site.register(models.Artical,Artical)
admin.site.register(models.Comment,Comment)

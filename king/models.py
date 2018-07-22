from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
import PIL

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(max_length=32,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth','username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Category(models.Model):  #类型；部门
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)

    def __str__(self):
        return "%s %s" %(self.name,self.url)
    class Meta:
        verbose_name_plural = "类别"

class Plate(models.Model):
    category = models.ForeignKey("Category",related_name="plate")
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    def __str__(self):
        return "%s %s" % (self.name, self.url)
    class Meta:
        verbose_name = "板块"


class Artical_tag(models.Model):    #文章标签
    tag = models.CharField(max_length=16)
    def __str__(self):
        return "%s" % (self.tag)

    class Meta:
        verbose_name = "标签"

class Artical(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    plate = models.ForeignKey("Plate",related_name='plate_artical')
    tags = models.ManyToManyField(Artical_tag,related_name='tag_atrical')
    publishTime = models.DateTimeField(auto_now_add=True)
    # title_image = models.ImageField(height_field=None,width_field=None,blank=True,null=True)
    title_image = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return "%s %s" % (self.title, self.plate)
    class Meta:
        verbose_name = "文章表"

class Comment(models.Model):
    artical = models.ForeignKey("Artical")
    user = models.ForeignKey("MyUser")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=256)
    parent = models.ForeignKey("self",related_name='comment',blank=True,null=True,)
    def __str__(self):
        return (self.content)
    class Meta:
        verbose_name_plural = "评论表"



class Artical_image(models.Model):

    img = models.ImageField(height_field=None,width_field=None,blank=True,null=True,upload_to='image/%Y/%m/%d/')

    def __str__(self):
        return "%s/%s"%(self.img.path,self.img.name)





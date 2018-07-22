# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=255, unique=True)),
                ('username', models.CharField(max_length=32, blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('publishTime', models.DateTimeField(auto_now_add=True)),
                ('title_image', models.CharField(max_length=128, blank=True, null=True)),
            ],
            options={
                'verbose_name': '文章表',
            },
        ),
        migrations.CreateModel(
            name='Artical_image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='image/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Artical_tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tag', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': '标签',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '类别',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=256)),
                ('artical', models.ForeignKey(to='king.Artical')),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='comment', to='king.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=32)),
                ('category', models.ForeignKey(related_name='plate', to='king.Category')),
            ],
            options={
                'verbose_name': '板块',
            },
        ),
        migrations.AddField(
            model_name='artical',
            name='plate',
            field=models.ForeignKey(related_name='plate_artical', to='king.Plate'),
        ),
        migrations.AddField(
            model_name='artical',
            name='tags',
            field=models.ManyToManyField(related_name='tag_atrical', to='king.Artical_tag'),
        ),
    ]

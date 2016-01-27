# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('contents', models.CharField(max_length=2048)),
                ('previous_lesson', models.ForeignKey(to='api.Lesson', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TriedLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('tries', models.IntegerField(default=0)),
                ('is_done', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(to='api.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('django_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('tried_lessons', models.ManyToManyField(to='api.Lesson', through='api.TriedLesson')),
            ],
        ),
        migrations.AddField(
            model_name='triedlesson',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
    ]

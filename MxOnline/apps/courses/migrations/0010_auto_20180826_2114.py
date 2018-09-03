# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-26 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='need_know',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8bfe\u7a0b\u9700\u77e5'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6559\u5e08\u7684\u8bdd'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-30 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_teacher_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.TextField(verbose_name='\u673a\u6784\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u673a\u6784\u540d\u79f0'),
        ),
    ]
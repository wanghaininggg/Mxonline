# _*_ coding: utf-8 _*_
#__author__:"whn"
#date: 2018/8/16

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name']
    list_filter = ['add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name']
    list_filter = ['click_nums', 'fav_nums', 'category', 'city__name', 'add_time']
    relfield_style = 'fk-ajax'  # 作为外键时下拉式变为搜索式 数据量过大时使用


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name']
    list_filter = ['work_company', 'work_position']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
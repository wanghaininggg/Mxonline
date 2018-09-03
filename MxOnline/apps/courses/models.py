# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    """
    课程表
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=100, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情',width=600, height=300, toolbars="full", imagePath="courses/ueditor/", filePath="courses/ueditor", default='')
    notice = models.CharField(max_length=200, verbose_name=u'课程公告', null=True, blank=True)
    degree = models.CharField(max_length=5, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')),
                              verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(max_length=100, upload_to="images/courses/%Y/%m", verbose_name=u'封面')
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name=u'课程种类')
    tag = models.CharField(default="", max_length=20, null=True, blank=True, verbose_name=u"课程标签")
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    need_know = models.CharField(max_length=50, verbose_name=u'课程需知', null=True, blank=True)
    teacher_tell = models.CharField(max_length=50, verbose_name=u'教师的话', null=True, blank=True)
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_learn_users(self):
        # 获取学习课程的学生数
        return self.usercourse_set.all()[:8]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def get_course_lesson_nums(self):
        # 获取课程所有章节数目
        return self.lesson_set.all().count()
    get_course_lesson_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description = "跳转"

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True    # 不会生成表


class Lesson(models.Model):
    """
    章节表
    """
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    """
    视频表
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    """
    资源表
    """
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = u'课程资源'

    def __unicode__(self):
        return self.name

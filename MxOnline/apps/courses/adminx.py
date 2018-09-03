# _*_ coding: utf-8 _*_
#__author__:"whn"
#date: 2018/8/16
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'get_course_lesson_nums', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time', 'go_to']
    search_fields = ['name']
    list_filter = ['degree', 'add_time', 'students', 'fav_nums']
    ordering = ['-click_nums']
    list_editable = ['degree']  # 列表页直接修改
    readonly_fields = ['click_nums']   # 只读
    exclude = ['fav_nums']  # 详情页不现实的字段
    refresh_times = [3, 5]  # 定时刷新页面
    inlines = [LessonInLine, CourseResourceInline]  # 关联多个表
    style_fields = {"detail": "ueditor"}
    import_excel = True

    def queryset(self):
        # 返回非轮播图的数据
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses = Course.objects.filter(course_org = course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass    # 写自己的逻辑
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['id', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name']
    list_filter = ['degree', 'add_time', 'students', 'fav_nums']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']   # 只读
    exclude = ['fav_nums']  # 详情页不现实的字段
    inlines = [LessonInLine, CourseResourceInline]

    def queryset(self):
        # 返回轮播图的数据
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner = True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'url', 'add_time']
    search_fields = ['name']
    list_filter = ['lesson__name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['name']
    list_filter = ['course__name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
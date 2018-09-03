# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
import json
# Create your views here.


class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):

        all_courses = Course.objects.all().order_by("-add_time") # 全部课程
        hots_courses = all_courses.order_by("fav_nums")[:3] # 热门课程

        # 搜索课程筛选
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程列表分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {'all_courses': courses,
                                                    'sort': sort,
                                                    'hot_courses': hots_courses})


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag
        relate_course = None
        if tag:
            relate_course = Course.objects.filter(tag=tag)[0]

        # 判断是否添加收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course = True
        return render(request, 'course-detail.html', {'course': course,
                                                      'has_fav_org': has_fav_org,
                                                      'has_fav_course': has_fav_course,
                                                      'relate_course': relate_course})


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    登录后才能访问
    """
    @staticmethod
    def get(request, course_id):

        course = Course.objects.get(id=int(course_id))

        # 关联用户与课程
        user_course =UserCourse.objects.filter(user=request.user, course=course)
        if not user_course: # 如果没有存在关联加入
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 学习本门课程的同学学习的其它课程
        user_cousers =UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_cousers.course.id for user_cousers in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {'course': course,
                                                     'all_resources': all_resources,
                                                     'relate_courses': relate_courses})


class CourseCommentView(LoginRequiredMixin, View):
    """
    评论
    """
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {'course': course,
                                                     'all_resources': all_resources,
                                                       'all_comment': all_comment})


class AddCommentsView(View):
    """
    添加评论
    """
    def post(self, request):

        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}))

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '评论成功'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '评论失败'}))


class VideoPlayView(View):
    @staticmethod
    def get(request, video_id):
        video = Video.objects.filter(id=video_id)[0]
        course = video.lesson.course

        # 学习本门课程的同学学习的其它课程
        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_cousers.course.id for user_cousers in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {'course': course,
                                                     'all_resources': all_resources,
                                                     'relate_courses': relate_courses,
                                                     'video': video})


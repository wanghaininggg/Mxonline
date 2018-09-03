# _*_ coding:utf-8 _*_
#__author__:"whn"
#date: 2018/8/25
from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentsView, VideoPlayView
urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),    #  课程列表页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course-detail"),  # 教师描述
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),       # 课程章节信息
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),       # 课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"), # 添加评论
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),  # 课程章节信息
]
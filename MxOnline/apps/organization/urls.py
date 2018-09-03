# _*_ coding:utf-8 _*_
#__author__:"whn"
#date: 2018/8/24
from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),    # 课程机构列表
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),        # 添加用户询问
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),     # 机构主页
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),      # 机构课程
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),  # 机构描述
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),  # 教师描述
    url(r'^add_fav/$', AddFavView.as_view(), name="org_add_fav"),

    # 讲师列表页
    url(r'^teacher_list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),  # 教师详情
]
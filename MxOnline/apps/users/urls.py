# _*_ coding:utf-8 _*_
#__author__:"whn"
#date: 2018/8/28

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UserMycourseView
from .views import UserFavOrgView, UserFavCourseView, UserFavTeacherView, UserMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),  # 用户信息

    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),    # 用户上传图片

    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),     # 用户个人中心修改密码

    url(r'^send_email_code/$', SendEmailCodeView.as_view(), name="send_email_code"),     # 发送邮箱验证码

    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"), # 修改邮箱

    url(r'^mycourse/$', UserMycourseView.as_view(), name="user_mycourse"), # 个人课程

    url(r'^myfav/org/$', UserFavOrgView.as_view(), name="user_fav_org"),   # 个人收藏——机构

    url(r'^myfav/course/$', UserFavCourseView.as_view(), name="user_fav_course"),  # 个人收藏——课程

    url(r'^myfav/teacher/$', UserFavTeacherView.as_view(), name="user_fav_teacher"),  # 个人收藏——教师

    url(r'^message/$', UserMessageView.as_view(), name="user_message"),  # 个人消息
]
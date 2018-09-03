# _*_ coding:utf-8 _*_
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm,ModifyForm, UploadImageForm, UserInfoForm
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
# Create your views here.


class CustomBackend(ModelBackend):
    """
    重写认证 加入邮箱可登录
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    用户激活
    """
    @staticmethod
    def get(request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, "active_success.html")
        else:
            return render(request, "active_fail.html")


class RegisterView(View):
    """
    注册视图
    """
    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    @staticmethod
    def post(request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            # 发送注册邮件
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    """
    退出登录
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """
    登录视图
    """
    @staticmethod
    def get(request):
        return render(request, 'login.html', {})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": u"用户未激活！"})
            else:
                return render(request, "login.html", {"msg": u"用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    """
    忘记密码
    """
    @staticmethod
    def get(request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    @staticmethod
    def post(request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


class ResetView(View):
    """
    重置密码
    """
    @staticmethod
    def get(request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")


class ModifyPwdView(View):
    """
    修改密码
    """
    @staticmethod
    def post(request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户视图
    """
    @staticmethod
    def get(request):
        return render(request, "usercenter-info.html", {})

    @staticmethod
    def post(request):
        userInfoForm = UserInfoForm(request.POST)
        if userInfoForm.is_valid():
            user = UserProfile.objects.get(id=request.user.id)
            user.nick_name = userInfoForm.cleaned_data.get('nick_name')
            user.birthday = userInfoForm.cleaned_data.get('birthday')
            user.gender = userInfoForm.cleaned_data.get('gender')
            user.address = userInfoForm.cleaned_data.get('address')
            user.mobile = userInfoForm.cleaned_data.get('mobile')
            user.email =userInfoForm.cleaned_data.get('email')
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail'}))


class UploadImageView(View):
    """
    用户修改头像
    """
    def post(self, request):
        image_from = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_from.is_valid():
            # image = image_from.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_from.save()
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail'}))


class UpdatePwdView(View):
    """
    个人中心修改密码
    """
    @staticmethod
    def post(request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '密码不一致'}))
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail'}))


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({"email": "邮箱已经被注册"}))
        send_register_email(email, "update_email")
        return  HttpResponse(json.dumps({"status": "success"}))


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'email': '验证码出错'}))


class UserMycourseView(LoginRequiredMixin, View):
    """
    个人中心——我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {'user_courses': user_courses})


class UserFavOrgView(LoginRequiredMixin, View):
    """
    个人收藏——机构
    """
    def get(self, request):
        fav_org = UserFavorite.objects.filter(user=request.user, fav_type=2)
        x = [x.fav_id for x in fav_org]
        all_user_fav_org = CourseOrg.objects.filter(id__in = x)
        current_page = 'org'
        return render(request, "usercenter-fav-org.html", {'all_user_fav_org': all_user_fav_org,
                                                           'current_page': current_page})


class UserFavCourseView(LoginRequiredMixin, View):
    """
    个人收藏——课程
    """
    def get(self, request):
        fav_org = UserFavorite.objects.filter(user=request.user, fav_type=1)
        x = [x.fav_id for x in fav_org]
        all_user_fav_course = Course.objects.filter(id__in = x)
        current_page = 'course'
        return render(request, "usercenter-fav-course.html", {'all_user_fav_course': all_user_fav_course,
                                                              'current_page': current_page})


class UserFavTeacherView(LoginRequiredMixin, View):
    """
    个人收藏——课程
    """
    def get(self, request):
        fav_org = UserFavorite.objects.filter(user=request.user, fav_type=3)
        x = [x.fav_id for x in fav_org]
        all_user_fav_teacher = Teacher.objects.filter(id__in = x)
        current_page = 'teacher'
        return render(request, "usercenter-fav-teacher.html", {'all_user_fav_teacher': all_user_fav_teacher,
                                                               'current_page': current_page})


class UserMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        # 用户个人和全局消息
        all_message = UserMessage.objects.filter(Q(user=request.user.id)|Q(user=0))

        # 用户进入个人消息后清空唯独消息的记录
        all_unread_message = all_message.filter(has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        # 对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)
        message= p.page(page)

        return render(request, "usercenter-message.html", {'all_message': message})


class IndexView(View):
    """
    慕学在线网首页
    """
    def get(self, request):
        # 去除轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses= Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {'all_banners': all_banners,
                                              'courses': courses,
                                              'banner_courses': banner_courses,
                                              'course_orgs': course_orgs})


def page_not_found(request):
    # 全局4.0处理函数
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response







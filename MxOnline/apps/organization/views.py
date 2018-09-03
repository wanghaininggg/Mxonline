# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite
from courses.models import Course
import json
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    @staticmethod
    def get(request):
        all_orgs = CourseOrg.objects.all()      # 课程机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_citys = CityDict.objects.all()      # 城市

        # 机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))        # 筛选

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-courses")

        org_nums = all_orgs.count() # 筛选后的数量

        # 对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request = request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {"all_orgs": orgs,
                                                 "all_citys": all_citys,
                                                 "org_nums": org_nums,
                                                 "city_id": city_id,
                                                 "category": category,
                                                 "hot_orgs": hot_orgs,
                                                 "sort": sort})


class AddUserAskView(View):
    """
    添加用户咨询
    """
    @staticmethod
    def post(request):
        user_ask_form = UserAskForm(request.POST)
        print request.POST
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            print user_ask
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            print user_ask_form.errors
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加出错'}))


class OrgHomeView(View):
    """
    机构首页
    """
    @staticmethod
    def get(request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teaches = course_org.teacher_set.all()[:1]

        # 判断是否添加收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {'all_course': all_courses,
                                                                'all_teacher': all_teaches,
                                                                'course_org':course_org,
                                                                'current_page': current_page,
                                                                'has_fav': has_fav})


class OrgCourseView(View):
    """
    机构课程列表页
    """
    @staticmethod
    def get(request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]

        # 判断是否添加收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {'all_course': all_courses,
                                                             'course_org': course_org,
                                                             'current_page': current_page,
                                                             'has_fav': has_fav})


class OrgDescView(View):
    """
    机构介绍页
    """
    @staticmethod
    def get(request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否添加收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html", {'course_org': course_org,
                                                           'current_page': current_page,
                                                           'has_fav': has_fav})


class OrgTeacherView(View):
    """
    机构教师
    """
    @staticmethod
    def get(request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teaches = course_org.teacher_set.all()

        # 判断是否添加收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {'all_teacher': all_teaches,
                                                            'course_org': course_org,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav})


class AddFavView(View):
    """
    用户收藏
    """
    @staticmethod
    def post(request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}))
        else:
            # 查找是否收藏
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                # 如果已经存在，表示用户取消收藏
                exist_records.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '取消收藏'}))
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    if int(fav_type) == 1:
                        course = Course.objects.get(id = int(fav_id))
                        course.fav_nums += 1
                        course.save()
                    elif int(fav_type) == 2:
                        org = CourseOrg.objects.get(id = int(fav_id))
                        org.fav_nums += 1
                        org.save()
                    elif int(fav_type) == 3:
                        teacher = Teacher.objects.get(id = int(fav_id))
                        teacher.fav_nums += 1
                        teacher.save()
                    return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏成功'}))
                else:
                    return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏失败'}))


class TeacherListView(View):
    """
    教师列表
    """
    @staticmethod
    def get(request):

        all_teachers = Teacher.objects.all()

        # 机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|Q(work_company__icontains=search_keywords))

        sort= request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by("-click_nums")

        # 热门讲师
        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")[:3]

        # 对教师列表分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        orgs = p.page(page)

        return render(request, "teachers-list.html", {'all_teachers': orgs,
                                                      'sorted_teacher': sorted_teacher,
                                                      'sort': sort})


class TeacherDetailView(View):
    """
    教师详情
    """
    @staticmethod
    def get(request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)

        teacher.click_nums += 1 # 教师点击访问数加1
        teacher.save()

        all_courses = teacher.course_set.all()
        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")[:3]

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id), fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
                has_fav_org = True

        return render(request, "teacher-detail.html", {'teacher': teacher,
                                                       'all_courses': all_courses,
                                                       'sorted_teacher': sorted_teacher,
                                                       'has_fav_teacher': has_fav_teacher,
                                                       'has_fav_org': has_fav_org})



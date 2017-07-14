#coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
from django.db.models import Q


from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()

        #热门机构
        hot_orgs = all_org.order_by('-click_nums')[:4]

        #机构搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
           all_org = all_org.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords))

        #筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        #筛选类别
        category = request.GET.get('ct', "")
        if category:
            all_org = all_org.filter(category=category)

        #学习人数，课程数
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-students")
            elif sort == 'courses':
                all_org = all_org.order_by('-course_nums')

        org_number = all_org.count()

        #分页操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 3,request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_org':orgs,
            'all_city':all_city,
            'org_number':org_number,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True) #进行数据库的保存，节省时间，是用modelform。
            print u'添加数据了'
            return HttpResponse("{'status':'success'}", content_type='application/json') #返回的数据格式
        else:
            # return HttpResponse("{'status':'fail','msg':{0}}".format(userask_form.errors))
            return HttpResponse("{'status':'fail','msg':'添加出错'}")



class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False #判断用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False  # 判断用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False  # 判断用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })



class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False  # 判断用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org':course_org,
            'current_page': current_page,
            'all_teachers':all_teachers,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏，和用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户是否登录
            # return HttpResponse("{'status':'fail','msg':'用户未登录'}", content_type='application/json')
            dict_json = {'status':'fail','msg':'用户未登录'}
            return JsonResponse(dict_json)
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录存在就取消用户收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.filter(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.filter(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.filter(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            dict_json = {'status': 'success', 'msg': '收藏'}
            return JsonResponse(dict_json)
            # return HttpResponse("{'status':'success','msg':'取消收藏'}",content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.filter(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.filter(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.filter(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                dict_json = {'status': 'success', 'msg': '已收藏'}
                return JsonResponse(dict_json)
                # return HttpResponse("{'status':'success','msg':'收藏'}",content_type='application/json')
            else:
                dict_json = {'status': 'fail', 'msg': '收藏出错'}
                return JsonResponse(dict_json)
                # return HttpResponse("{'status':'fail','msg':'收藏出错'}",content_type='application/json')



class TeacherLlistView(View):
    """
    讲师列表页
    """
    def get(self, request):
        teachers = Teacher.objects.all()

        fav_teachers = teachers.order_by('-fav_nums')[:3]

        #教师搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = teachers.filter(Q(name__icontains=keywords)|Q(work_company__icontains=keywords)|
                                       Q(work_position__icontains=keywords))

        #教师人气排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                teachers = teachers.order_by('-click_nums')


        teachers_count = teachers.count()

        # 分页操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, 3, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers':teachers,
            'sort':sort,
            'teachers_count':teachers_count,
            'fav_teachers':fav_teachers,
        })
        pass


class TeacherDetailView(View):

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums +=1
        teacher.save()

        has_fav = False  # 判断用户是否收藏_课程
        has_fav_2 = False  # 判断用户是否收藏_机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher_id), fav_type=3):
                has_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
                has_fav_2 = True

        all_courses = Course.objects.filter(teacher=teacher)

        fav_teachers =  Teacher.objects.all().order_by('-fav_nums')[:3]

        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'fav_teachers':fav_teachers,
            'all_courses':all_courses,
            'has_fav':has_fav,
            'has_fav_2':has_fav_2,
        })
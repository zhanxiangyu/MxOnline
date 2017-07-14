#coding:utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from django.db.models import Q

from .models import Course,CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        #课程搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        #热门和参与人数
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by("-students")
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')


        # 分页操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)


        return render(request, 'course-list.html', {
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        has_fav = False  # 判断用户是否收藏_课程
        has_fav_2 = False #判断用户是否收藏_机构
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_2 = True

        #增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag).exclude(pk=course.id)[:1]
            if not relate_coures:
                relate_coures = []
        else:
            relate_coures = []



        return render(request, 'course-detail.html', {
            'course':course,
            'relate_coures':relate_coures,
            'has_fav':has_fav,
            'has_fav_2':has_fav_2,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程_章节_详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students +=1
        course.save()

        #查询用户是否关联该课程
        user_course = UserCourse.objects.filter(user = request.user, course = course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resource = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [ user_course.user.id for user_course in user_courses ]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [ all_user_course.course.id for all_user_course in all_user_courses ]

        relate_courses = Course.objects.filter(id__in= course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'all_resource':all_resource,
            'relate_courses':relate_courses,
        })



class CourseCommentCiew(LoginRequiredMixin, View):
    """
    课程_章节_评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resource = CourseResource.objects.filter(course=course)

        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html', {
            'course':course,
            'all_resource':all_resource,
            'all_comments':all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    """
    添加课程评论
    """
    def post(self, request):

        if not request.user.is_authenticated():
            dict_json = {'status': 'fail', 'msg': '用户未登录'}
            return JsonResponse(dict_json)

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')

        if course_id > 0 and comments:
            course_comment = CourseComments()
            course_comment.course = Course.objects.get(pk=course_id)
            course_comment.user = request.user
            course_comment.comments =  comments
            course_comment.save()
            dict_json = {'status': 'success', 'msg': '添加成功'}
            return JsonResponse(dict_json)
        else:
            dict_json = {'status': 'fail', 'msg': '添加失败'}
            return JsonResponse(dict_json)



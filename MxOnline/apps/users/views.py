#coding:utf-8
import json

from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginFrom,RegisterFrom,ForgetFrom,ModifyFrom, UserInfoFrom
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import ImageUploadFrom
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) #完成并集
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class RegisterView(View):
    def get(self, request):
        register_from =RegisterFrom()
        return render(request, 'register.html', {'register_from':register_from })
    def post(self, request):
        register_from = RegisterFrom(request.POST)
        if register_from.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': u'用户已存在','register_from': register_from})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False #设置用户未激活
            user_profile.save() #保存到我们的数据库中

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎注册我的网站'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        else:
            # register_from = RegisterFrom()  #注意点容易出错，这里不需要在进行实例化了
            return render(request, 'register.html', {'register_from': register_from})
        pass

class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_file.html')
        return  render(request, 'login.html',)
        pass
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})
        else:
            return render(request, 'active_file.html')


class ModifyView(View):
    """
    修改密码
    """

    def post(self, request):
        modify_form = ModifyFrom(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg':u'两次输入的密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'msg': u'两次输入的密码不一致'})
        pass


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):  #基于类的调用
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        login_form = LoginFrom(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)  # 对用户名和密码进行验证，成功返回对象，不成功返回None
            if user is not None:
                if user.is_active:
                    login(request, user)  # 将用户信息放入request里面
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活，请到邮箱查看激活链接'})
            else:
                return render(request, 'login.html', {'msg': u'用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})
        pass

class ForgetView(View):
    def get(self,request):
        forget_form = ForgetFrom()
        return render(request, 'forgetpwd.html', {'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetFrom(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form':forget_form})
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         print user_name,'dsafas'
#         user = authenticate(username = user_name,password = pass_word) #对用户名和密码进行验证，成功返回对象，不成功返回None
#         if user is not None:
#             login(request, user) #将用户信息放入request里面
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg':u'用户名或者密码错误'})
#         pass
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户信息
    """
    def get(self, request):

        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_forms = UserInfoFrom(request.POST, instance=request.user)
        if user_info_forms.is_valid():
            user_info_forms.save()
            dict_json = {'status': 'success', 'msg': '修改成功'}
            return JsonResponse(dict_json)
        else:
            return HttpResponse(json.dumps(user_info_forms.errors), content_type="application/json")



class ImageUploadView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        #使用modelform
        # image_forms = ImageUploadFrom(request.POST, request.FILES, instance=request.user) #rinstance=equest.user 是modleform里面对应的model
        # if image_forms.is_valid():
        #     image_forms.save() #就可以直接进行保存
        #     dict_json = {'status': 'success', 'msg': '修改成功'}
        #     return JsonResponse(dict_json)


        #不使用modelform
        image_forms = ImageUploadFrom(request.POST, request.FILES)

        if image_forms.is_valid():
            image = image_forms.cleaned_data['image']
            request.user.image = image
            request.user.save()
            dict_json = {'status': 'success', 'msg': '修改成功'}
            return JsonResponse(dict_json)


class UpdatePwdView(LoginRequiredMixin, View):
    """
    修改用户密码，个人中心
    """
    def post(self, request):
        modify_form = ModifyFrom(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                dict_json = {'status': 'fail', 'msg': '两次密码不一样'}
                return JsonResponse(dict_json)
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            dict_json = {'status': 'success', 'msg': '修改成功'}
            return JsonResponse(dict_json)
        else:
            # dict_json = {'status': 'fail', 'msg': '输入错误'}
            # dict_json = json.dumps(modify_form.errors)
            # return JsonResponse(dict_json)
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")

class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email=email, send_type='update')
        dict_json = {'status': 'success', 'msg': '发送成功'}
        return JsonResponse(dict_json)


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人中心的邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code)
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            dict_json = {'status':'success', 'msg': '修改成功'}
            return JsonResponse(dict_json)
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type="application/json")


class UserCouseView(LoginRequiredMixin, View):
    """
    显示用户课程
    """
    def get(self, request):
        user = request.user
        usercourses = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {
            'usercourses':usercourses,
        })


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户个人中心-收藏机构
    """
    def get(self, request):
        user = request.user
        userfav_orgs = UserFavorite.objects.filter(user=user, fav_type=2)
        org_list = []
        for userfav_org in userfav_orgs:
            fav_id = userfav_org.fav_id
            org = CourseOrg.objects.get(id=fav_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
                'org_list':org_list,
        })

class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户个人中心-收藏教师
    """
    def get(self, request):
        user = request.user
        userfav_teachers = UserFavorite.objects.filter(user=user, fav_type=3)
        teacher_list = []
        for userfav_teacher in userfav_teachers:
            fav_id = userfav_teacher.fav_id
            teacher = Teacher.objects.get(id=fav_id)
            teacher_list.append(teacher)

        return render(request, "usercenter-fav-teacher.html", {
            'teacher_list':teacher_list,
        })


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户个人中心-收藏公开课程
    """
    def get(self, request):
        user = request.user
        userfav_courses = UserFavorite.objects.filter(user=user, fav_type=1)
        course_list = []
        for userfav_course in userfav_courses:
            fav_id = userfav_course.fav_id
            course = Course.objects.get(id=fav_id)
            course_list.append(course)

        return render(request, "usercenter-fav-course.html", {
                'course_list':course_list,
        })


class UserMessageView(LoginRequiredMixin, View):
    """
    用户个人中心-我的消息
    """
    def get(self, request):
        user = request.user
        all_message = UserMessage.objects.filter(user=user.id)

        #对已经查看的消息设置为已读
        unread_messages = all_message.filter(has_read=False)
        for unread_message in unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页操作
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 3, request=request)

        all_messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'all_messages':all_messages,
        })

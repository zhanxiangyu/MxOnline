# -*- coding:utf-8 -*-
# __author__ = 'zhan'
# __date__ = '17-7-9 下午9:51'
from django.conf.urls import url,include

from .views import UserInfoView,ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import UserCouseView, UserFavOrgView,UserFavTeacherView,UserFavCourseView,UserMessageView

urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    #用户修改头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),

    #修改用户密码，个人中心
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='uploda_image'),

    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code' ),

    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #用户课程
    url(r'^user_course/$', UserCouseView.as_view(), name='user_course'),

    #用户收藏--机构
    url(r'^userfav/org/$', UserFavOrgView.as_view(), name='user_fav_org'),

    #用户收藏--教师
    url(r'^userfav/teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),

    #用户收藏--公开课程
    url(r'userfav/course/$', UserFavCourseView.as_view(), name='user_fav_course'),

    #我的消息
    url(r'user/message/$', UserMessageView.as_view(), name='user_message')
]
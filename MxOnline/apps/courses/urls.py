#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/7/2 10:22'

from django.conf.urls import url,include

from .views import CourseListView,CourseDetailView, CourseInfoView, CourseCommentCiew,AddCommentView


urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),

    #课程章节评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentCiew.as_view(), name='course_comment'),

    #添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment')

]
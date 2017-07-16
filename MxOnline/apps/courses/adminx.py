#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/5/8 9:37'

import xadmin
from .models import Course,Lesson,Video,CourseResource


class CourseAdmin(object):
    list_display = ('name','desc','detail','degree','learn_times','students','fav_nums','click_nums')
    search_fields = ('name','desc','detail','degree','learn_times','students','fav_nums','click_nums')
    list_filter = ('name','desc','detail','degree','learn_times','students','fav_nums','click_nums')
    ordering = ['-click_nums'] #降序排列
    pass


class LessonAdmin(object):
    list_display = ('course', 'name', 'add_time')
    search_fields = ('course', 'name')
    list_filter =('course__name', 'name', 'add_time')
    pass


class VideoAdmin(object):
    list_display = ('lesson', 'name', 'add_time')
    search_fields = ('lesson', 'name')
    list_filter =('lesson__name', 'name', 'add_time')
    pass


class CourseResourceAdmin(object):
    list_display = ('course', 'name', 'download','add_time')
    search_fields = ('course', 'name', 'download')
    list_filter =('course__name', 'name', 'download','add_time')
    pass


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

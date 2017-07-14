#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/5/8 9:59'

import xadmin
from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ('name','desc','add_time')
    search_fields = ('name','desc',)
    list_filter = ('name','desc','add_time')
    pass


class CourseOrgAdmin(object):
    list_display = ('name', 'desc', 'click_nums','fav_nums','city','add_time')
    search_fields = ('name', 'desc', 'click_nums','fav_nums','city')
    list_filter =('name', 'desc', 'click_nums','fav_nums','city','add_time')
    pass


class TeacherAdmin(object):
    list_display = ('org', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time')
    search_fields = ('org', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums')
    list_filter =('org', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time')
    pass


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

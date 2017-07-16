#coding:utf-8
# __author__ = 'zhan'
# __date__ = '2017/5/8 0:50'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner


class BaseSetting(object):
    enable_themes = True #开启主题功能
    use_bootswatch = True #增加主题功能的选择性

class GlobalSetting(object):
    site_title = '后台管理系统'
    site_footer = '在线教育网'
    menu_style = 'accordion' #将APP里面的模块收集到app所在的列表里面

class EmailVerifyRecordAdmin(object):
    list_display = ('code','email','send_type','send_time')
    search_fields = ('code','email','send_type')
    list_filter = ('code','email','send_type','send_time')
    model_icon = 'fa fa-archive' #修改图标
    pass


class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index','add_time')
    search_fields = ('title', 'image', 'url', 'index')
    list_filter = ('title', 'image', 'url', 'index','add_time')
    pass


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting) #注册主题功能
xadmin.site.register(views.CommAdminView, GlobalSetting) #修改后台标题，和公司

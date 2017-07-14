#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/5/8 14:00'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginFrom(forms.Form):
    username = forms.CharField(required=True) #这是一个必填项目
    password = forms.CharField(required=True, min_length=5)


class RegisterFrom(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})


class ForgetFrom(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class ModifyFrom(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ImageUploadFrom(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoFrom(forms.ModelForm):
    """
    验证个人中心修改数据
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']

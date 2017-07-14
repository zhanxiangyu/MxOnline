#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/7/1 9:53'
import re
from django import forms

from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=3, max_length=50)
#     pass


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        手机号码的验证
        """
        mobile = self.cleaned_data['mobile']
        GET_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(GET_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机格式错误', code='mobile_invalid')
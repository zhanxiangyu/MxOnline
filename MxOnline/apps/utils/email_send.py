#coding:utf-8
#__author__ = 'zhan'
#__date__ = '2017/5/8 17:18'
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    length = len(chars)
    random = Random()
    for i in range(randomlength):
        str+= chars[random.randint(0,length-1)]

    return str

def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = '制作网站激活链接'
        email_body = '请点击激活链接： http://127.0.0.1:8000/active/{}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM,[email])
        if send_status:
            print u'状态码成功'
            pass
    elif send_type == 'forget':
        email_title = '制作网站找回密码功能'
        email_body = '请点击找回链接： http://127.0.0.1:8000/reset/{}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print u'状态码成功'
            pass
    elif send_type == 'update':
        email_title = '制作网站修改邮箱'
        email_body = '邮箱验证码： {}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print u'状态码成功'
            pass
# _*_ coding:utf-8 _*_
#__author__:"whn"
#date: 2018/8/17
import random
import string
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FORM


def ran_char():
    # 随机生成字符串
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt


def send_register_email(email, send_type="register"):
    # 发送邮件
    email_record = EmailVerifyRecord()
    code = ran_char()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        """
        注册
        """
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的帐号：http://127.0.0.1:8000/active/{0}".format(code)
        send_mail(email_title, email_body, EMAIL_FORM, [email], fail_silently=False)

    elif send_type == "forget":
        """
        忘记密码
        """
        email_title = "慕学在线网注册密码激活链接"
        email_body = "请点击下面的重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_mail(email_title, email_body, EMAIL_FORM, [email], fail_silently=False)

    elif send_type == "update_email":
        """
        修改密码
        """
        email_title = "慕学在线网邮箱修改验证码"
        email_body = "你的邮箱验证码为{0}".format(code)
        send_mail(email_title, email_body, EMAIL_FORM, [email], fail_silently=False)

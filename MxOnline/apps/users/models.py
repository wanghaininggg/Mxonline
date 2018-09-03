# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户名
    """
    nick_name = models.CharField(max_length=50, default='', verbose_name=u'昵称')
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="male", verbose_name=u"性别")
    address = models.CharField(max_length=100, default=u"", verbose_name=u"地址", null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"手机")
    image = models.ImageField(upload_to="images/image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u"照片")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=20, choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'修改邮箱')), verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    轮播图
    """
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(max_length=100, upload_to="images/banner/%Y/%m", verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index= models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name


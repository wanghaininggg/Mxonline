# _*_ encoding:utf-8 _*_
#date: 2018/8/16
import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = u"慕学后台管理系统"
    site_footer = u"慕学在线网"
    menu_style = "accordion"


class EmainVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['email']
    list_filter = ['send_type', 'send_time']
    model_icon = 'fa fa-address-book-o' # 修改图标


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title']
    list_filter = ['add_time','index']
    model_icon = 'fa fa-file-photo-o'


xadmin.site.register(EmailVerifyRecord, EmainVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
from django.contrib import admin

from project_models.models import UserInfo, PositionInfo, MachineGroupInfo, HostInfo, YuanXingInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'position']


class HostInfoAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'host']


# Register your models here.
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PositionInfo)
admin.site.register(MachineGroupInfo)
admin.site.register(HostInfo, HostInfoAdmin)
admin.site.register(YuanXingInfo)

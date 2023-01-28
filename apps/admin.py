from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group as DefaultGroup
from .models import Group, Admin, User, Settings, InvatedMember

admin.site.unregister(DefaultGroup)


class GroupAdmin(ImportExportModelAdmin, ModelAdmin):
    readonly_fields = ('title', 'username', 'chat_id')


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ('id', 'get_full_name', 'username', 'is_staff')
    # exclude = ('date_joined', 'last_login',)
    actions = [
        'activate_users',
    ]

    def activate_users(self, request, queryset):
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))

    activate_users.short_description = 'Activate Users'  # type: ignore


class UserModelAdmin(ImportExportModelAdmin, ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_joined')
    readonly_fields = ('first_name', 'last_name', 'telegram_id')
    search_fields = ('first_name', 'last_name')
    list_filter = ('date_joined',)


def get_user(user_id):
    return User.objects.get(telegram_id=user_id)


class InvatedMemberModelAdmin(ImportExportModelAdmin, ModelAdmin):
    list_display = ('first_name', 'invated_users_count')

    readonly_fields = []

    def first_name(self, obj):
        user = get_user(obj.telegram)
        return user.first_name


admin.site.register(User, UserModelAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Admin, CustomUserAdmin)
admin.site.register(InvatedMember, InvatedMemberModelAdmin)
admin.site.register(Settings, ImportExportModelAdmin)

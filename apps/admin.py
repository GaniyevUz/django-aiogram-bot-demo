from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group as DefaultGroup
from .models import Group, Admin, User, Settings

admin.site.unregister(DefaultGroup)


class GroupAdmin(ImportExportModelAdmin, ModelAdmin):
    readonly_fields = ('title', 'username', 'chat_id')


admin.site.register(Group, GroupAdmin)


# dashboard.site.register(Admin, ImportExportModelAdmin)


@admin.register(Admin)
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


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',)
    readonly_fields = ('first_name', 'last_name', 'group', 'telegram_id')


admin.site.register(Settings, ImportExportModelAdmin)

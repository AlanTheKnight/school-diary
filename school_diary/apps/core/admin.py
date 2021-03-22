from django.contrib import admin

from . import models

admin.site.site_header = "Электронный дневник"
admin.site.index_title = "Панель администратора"
admin.site.enable_nav_sidebar = False


@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_type')
    list_filter = ('account_type',)


class UserAccountMixin(admin.ModelAdmin):
    list_display = ('account', 'surname', 'first_name')

    def first_name(self, obj):
        return obj.account.first_name

    def second_name(self, obj):
        return obj.account.second_name

    def surname(self, obj):
        return obj.account.surname


@admin.register(models.Students)
class StudentsAdmin(UserAccountMixin):
    list_filter = ('klass',)


@admin.register(models.Admins)
class AdminsAdmin(UserAccountMixin):
    ...


@admin.register(models.Teachers)
class TeachersAdmin(UserAccountMixin):
    list_filter = ('subjects',)


admin.site.register(models.Grades)
admin.site.register(models.Klasses)
admin.site.register(models.Lessons)
admin.site.register(models.AdminMessages)
admin.site.register(models.Controls)
admin.site.register(models.Subjects)
admin.site.register(models.Quarters)
admin.site.register(models.Groups)
admin.site.register(models.Homework)

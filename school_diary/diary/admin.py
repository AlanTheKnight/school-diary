from django.contrib import admin
from . import models


admin.site.site_header = "Электронный дневник"
admin.site.index_title = "Панель администратора"


@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_type')
    list_filter = ('account_type',)


@admin.register(models.Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'surname', 'grade')
    list_filter = ('grade',)


@admin.register(models.Administrators)
class AdministratorsAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'surname')


@admin.register(models.Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'surname')
    list_filter = ('subjects',)


admin.site.register(models.Grades)
admin.site.register(models.Marks)
admin.site.register(models.Lessons)
admin.site.register(models.AdminMessages)
admin.site.register(models.Controls)
admin.site.register(models.Subjects)
admin.site.register(models.Quarters)
admin.site.register(models.Groups)

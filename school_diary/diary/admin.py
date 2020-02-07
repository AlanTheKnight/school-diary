from django.contrib import admin
from .models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_type')
    list_filter = ('account_type',)


@admin.register(Students)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'surname', 'grade')
    list_filter = ('grade',)


admin.site.register(Teachers)
admin.site.register(Grades)
admin.site.register(Subjects)

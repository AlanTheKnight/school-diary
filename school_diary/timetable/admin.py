from django.contrib import admin
from .models import Lessons, BellsTimeTable


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('connection', 'day', 'subject')
    list_filter = ('connection', 'day', 'subject', 'number')


admin.site.register(BellsTimeTable)

from django.contrib import admin
from .models import Lessons, BellsTimeTable


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('klass', 'day', 'subject')
    list_filter = ('klass', 'day', 'subject', 'number')


admin.site.register(BellsTimeTable)

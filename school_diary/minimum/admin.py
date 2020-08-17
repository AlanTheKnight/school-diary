from django.contrib import admin
from . import models

@admin.register(models.Documents)
class MinimumAdmin(admin.ModelAdmin):
    list_display = ('subject', 'grade', 'term')
    list_filter = ('subject', 'term')

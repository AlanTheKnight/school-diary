from django.contrib import admin
from . import models


@admin.register(models.NotesGroup)
class NotesGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_author')

    def get_author(self, obj: models.NotesGroup):
        return obj.author.get_short_name()

    get_author.short_description = "Автор"


admin.site.register(models.Note)
admin.site.register(models.Category)

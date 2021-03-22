from django import forms
from . import models


class NotesGroupCreationForm(forms.ModelForm):
    class Meta:
        model = models.NotesGroup
        fields = ["category", "title", "public"]

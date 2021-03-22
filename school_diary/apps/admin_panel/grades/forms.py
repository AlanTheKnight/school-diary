from django import forms
from apps.core import models


class GradeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Klasses
        fields = ['number', 'letter', 'head_teacher', 'subjects', 'teachers']

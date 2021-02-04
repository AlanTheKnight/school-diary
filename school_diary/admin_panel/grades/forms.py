from django import forms
from core import models


class GradeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Klasses
        fields = ['number', 'letter', 'head_teacher', 'subjects', 'teachers']

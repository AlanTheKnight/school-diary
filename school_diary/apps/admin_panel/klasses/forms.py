from django import forms
from apps.core import models


class KlassCreationForm(forms.ModelForm):
    class Meta:
        model = models.Klasses
        fields = ('teachers', 'subjects', 'letter', 'number', 'head_teacher')
        help_texts = {
            'teachers': 'Зажмите клавишу Ctrl (или Command на Mac), чтобы выбрать несколько значений',
            'subjects': 'Зажмите клавишу Ctrl (или Command на Mac), чтобы выбрать несколько значений'
        }

from django import forms
from diary import models

bts4attr = {'class': 'form-control'}


class GradeCreationForm(forms.ModelForm):

    class Meta:
        model = models.Grades
        fields = ['number', 'letter', 'main_teacher', 'subjects', 'teachers']
        widgets = {
            'number': forms.Select(attrs=bts4attr),
            'letter': forms.Select(attrs=bts4attr),
            'main_teacher': forms.Select(attrs=bts4attr),
            'subjects': forms.SelectMultiple(attrs=bts4attr),
            'teachers': forms.SelectMultiple(attrs=bts4attr),
        }

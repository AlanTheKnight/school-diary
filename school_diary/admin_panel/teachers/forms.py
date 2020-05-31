from django import forms
from diary import models

bts4attr = {'class': 'form-control'}


class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = models.Teachers
        fields = ('first_name', 'surname', 'second_name', 'subjects')
        widgets = {
            'first_name': forms.TextInput(attrs=bts4attr),
            'surname': forms.TextInput(attrs=bts4attr),
            'second_name': forms.TextInput(attrs=bts4attr),
            'subjects': forms.SelectMultiple(attrs=bts4attr),
        }

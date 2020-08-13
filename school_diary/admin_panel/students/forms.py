from django import forms
from diary import models

bts4attr = {'class': 'form-control'}


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = models.Students
        fields = ('first_name', 'surname', 'second_name', 'grade')
        widgets = {
            'first_name': forms.TextInput(attrs=bts4attr),
            'surname': forms.TextInput(attrs=bts4attr),
            'second_name': forms.TextInput(attrs=bts4attr),
            'grade': forms.Select(attrs=bts4attr),
        }

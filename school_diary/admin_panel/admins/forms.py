from django import forms
from diary import models


bts4attr = {'class': 'form-control'}


class AdminsEditForm(forms.ModelForm):
    class Meta:
        model = models.Administrators
        fields = ('first_name', 'surname', 'second_name')
        widgets = {
            'first_name': forms.TextInput(attrs=bts4attr),
            'surname': forms.TextInput(attrs=bts4attr),
            'second_name': forms.TextInput(attrs=bts4attr),
        }

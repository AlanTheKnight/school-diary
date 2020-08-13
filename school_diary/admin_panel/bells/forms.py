from django import forms
from timetable import models

bts4attr = {'class': 'form-control'}


class BellCreateForm(forms.ModelForm):
    """Form for creating a new bell in timetable admin panel."""
    class Meta:
        model = models.BellsTimeTable
        fields = ('school', 'n', 'start', 'end')
        widgets = {
            'school': forms.Select(attrs=bts4attr),
            'n': forms.NumberInput(attrs={'class': 'form-control', 'max': "9", 'min': "1"}),
            'start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
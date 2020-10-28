from django import forms
from .models import Documents


sel_class = {'class': 'form-control custom-select'}
widgets = {
    'subject': forms.Select(attrs=sel_class),
    'grade': forms.Select(attrs=sel_class),
    'term': forms.Select(attrs=sel_class),
    'file': forms.FileInput(attrs={'class': 'form-control-file'}),
}


class GetMinimumForm(forms.ModelForm):
    class Meta:
        model = Documents
        exclude = ('file', )
        widgets = widgets


class MinimumCreationForm(forms.ModelForm):
    class Meta:
        fields = ('subject', 'grade', 'term', 'file')
        model = Documents
        widgets = widgets

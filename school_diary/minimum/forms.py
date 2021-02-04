from django import forms
from .models import Documents


class GetMinimumForm(forms.ModelForm):
    class Meta:
        model = Documents
        exclude = ('file', )


class MinimumCreationForm(forms.ModelForm):
    class Meta:
        fields = ('subject', 'grade', 'term', 'file')
        model = Documents

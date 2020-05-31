from django import forms
from news import models


bts4attr = {'class': 'form-control'}


class ArticleCreationForm(forms.ModelForm):
    """Form for creating a new post in news section."""
    class Meta:
        model = models.Publications
        fields = ('title', 'author', 'content', 'image', 'slug')
        widgets = {
            'title': forms.TextInput(attrs=bts4attr),
            'author': forms.TextInput(attrs=bts4attr),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'slug': forms.TextInput(attrs=bts4attr),
        }

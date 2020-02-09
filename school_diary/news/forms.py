from django import forms
from .models import Publications


class ArticleCreationForm(forms.ModelForm):

    class Meta:
        model = Publications
        fields = ('title', 'content', 'image', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'id':'title'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10, 'id':'content'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control-file', 'id':'image'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'id':'slug'}),
        }
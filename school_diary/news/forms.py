from django import forms
from .models import Publications


class ArticleCreationForm(forms.ModelForm):

    class Meta:
        model = Publications
        fields = ('title', 'author', 'content', 'image', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'id':'title', 'maxlength':'100'}),
            'author': forms.TextInput(attrs={'class':'form-control', 'id':'author', 'maxlength':'50'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10, 'id':'content', 'maxlength':'5000'}),
            'image': forms.FileInput(attrs={'class':'custom-file-input', 'id':'image', 'onchange':'show_delete_button();'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'id':'slug', 'maxlength':'100'}),
        }
from django import forms
from apps.news import models

bts4attr = {'class': 'form-control'}


class ArticleCreationForm(forms.ModelForm):
    """Form for creating a new post in news section."""
    class Meta:
        model = models.Publications
        fields = "__all__"
        help_texts = {
            "slug": "Уникальная ссылка на написанную статью (может состоять только " +
            "из букв латинского алфавита, дефисов и цифр)",
            "author": "Отображаемый автор статьи",
            "content": "Текст статьи, может использовать разметку MarkDown, а также CSS & HTML"
        }

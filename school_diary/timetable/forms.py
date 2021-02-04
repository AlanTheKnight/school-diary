from django import forms
from django.conf import settings
from timetable import models


bts_attrs = {'class': 'form-control'}


class GetTimeTableForm(forms.Form):
    grade = forms.ChoiceField(label="Класс:", choices=settings.GRADES, widget=forms.Select(attrs=bts_attrs))
    litera = forms.ChoiceField(label="Буква:", choices=settings.LETTERS, widget=forms.Select(attrs=bts_attrs))


class LessonCreateForm(forms.ModelForm):
    """Form for creating a new lesson in timetable admin panel."""
    class Meta:
        model = models.Lessons
        fields = ('klass', 'day', 'number', 'subject', 'classroom')

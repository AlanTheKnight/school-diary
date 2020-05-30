from django import forms
from news.models import Publications
from timetable.models import BellsTimeTable, Lessons
from diary import models


bts4attr = {'class': 'form-control'}


class ArticleCreationForm(forms.ModelForm):
    """Form for creating a new post in news section."""
    class Meta:
        model = Publications
        fields = ('title', 'author', 'content', 'image', 'slug')
        widgets = {
            'title': forms.TextInput(attrs=bts4attr),
            'author': forms.TextInput(attrs=bts4attr),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'slug': forms.TextInput(attrs=bts4attr),
        }


class LessonCreateForm(forms.ModelForm):
    """Form for creating a new lesson in timetable admin panel."""
    class Meta:
        model = Lessons
        fields = ('connection', 'day', 'number', 'subject', 'classroom')


class BellCreateForm(forms.ModelForm):
    """Form for creating a new bell in timetable admin panel."""
    class Meta:
        model = BellsTimeTable
        fields = ('school', 'n', 'start', 'end')
        widgets = {
            'school': forms.Select(attrs=bts4attr),
            'n': forms.NumberInput(attrs={'class': 'form-control', 'max': "9", 'min': "1"}),
            'start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


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


class AdminsEditForm(forms.ModelForm):
    class Meta:
        model = models.Administrators
        fields = ('first_name', 'surname', 'second_name')
        widgets = {
            'first_name': forms.TextInput(attrs=bts4attr),
            'surname': forms.TextInput(attrs=bts4attr),
            'second_name': forms.TextInput(attrs=bts4attr),
        }


class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = models.Teachers
        fields = ('first_name', 'surname', 'second_name', 'subjects')
        widgets = {
            'first_name': forms.TextInput(attrs=bts4attr),
            'surname': forms.TextInput(attrs=bts4attr),
            'second_name': forms.TextInput(attrs=bts4attr),
            'subjects': forms.SelectMultiple(attrs=bts4attr),
        }

from django import forms
from timetable import models


bts_attrs = {'class': 'form-control'}


class GetTimeTableForm(forms.Form):
    grade = forms.ChoiceField(label="Класс:", choices=[
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11)], widget=forms.Select(attrs=bts_attrs))
    litera = forms.ChoiceField(label="Буква:", choices=[
        ("А", "А"),
        ("Б", "Б"),
        ("В", "В"),
        ("Г", "Г"),
        ("Д", "Д"),
        ("Е", "Е"),
        ("Ж", "Ж"),
        ("З", "З"),
        ("И", "И"),
        ("К", "К")], widget=forms.Select(attrs=bts_attrs))


class LessonCreateForm(forms.ModelForm):
    """Form for creating a new lesson in timetable admin panel."""
    class Meta:
        model = models.Lessons
        fields = ('connection', 'day', 'number', 'subject', 'classroom')

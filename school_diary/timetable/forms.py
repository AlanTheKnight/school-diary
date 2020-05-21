from django import forms
from .models import Lessons, BellsTimeTable


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
        (11, 11)])
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
        ("К", "К")])


class LessonCreateForm(forms.ModelForm):

    class Meta:
        model = Lessons
        fields = ('connection', 'day', 'number', 'subject', 'classroom')


class BellCreateForm(forms.ModelForm):
    class Meta:
        model = BellsTimeTable
        fields = ('school', 'n', 'start', 'end')
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control', 'id': 'school'}),
            'n': forms.NumberInput(attrs={'class': 'form-control', 'id': 'n', 'max':"9", 'min':"1"}),
            'start': forms.TimeInput(attrs={'class': 'form-control', 'id': 'start', 'type':'time'}),
            'end': forms.TimeInput(attrs={'class': 'form-control', 'id': 'end', 'type':'time'}),
        }
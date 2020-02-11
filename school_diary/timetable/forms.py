from django import forms
from .models import Lessons

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
    litera = forms.ChoiceField(label="Литера:", choices=[
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
        fields = ('connection', 'day', 'number', 'start', 'end', 'subject', 'classroom')
        widgets = {
            'number':forms.NumberInput(attrs={'max':'8', 'min':'0'}),
            'start':forms.TimeInput(attrs={'type':'time'}),
            'end':forms.TimeInput(attrs={'type':'time'})
        }
from django import forms

from . import models
from .homework import HomeworkForm

__all__ = [
    "HomeworkForm", "DatePickForm", "LessonCreationForm",
    "QuarterSelectionForm", "GroupSelectionForm"
]


QUARTERS = [(1, "I"), (2, "II"), (3, "III"), (4, "IV")]


class DatePickForm(forms.Form):
    date = forms.DateField(
        label="Дата", widget=forms.DateInput(attrs={'type': 'date'}))


class LessonCreationForm(forms.ModelForm):
    deleteFile = forms.BooleanField(initial=False, required=False)

    """Form for creating/editing a lesson."""
    class Meta:
        model = models.Lessons
        fields = (
            'date', 'theme', 'control', 'is_planned', 'deleteFile'
        )
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': 'date'
            })
        }
        labels = {
            'h_file': 'Файл с домашним заданием',
            'date': 'Дата',
            'theme': 'Тема урока',
            'homework': 'Домашнее задание на создаваемый урок',
            'control': 'Вид работы',
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if models.Quarters.get_quarter_by_date(str(date)) is None:
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def save(self, commit=True, **kwargs):
        instance = super(LessonCreationForm, self).save(commit=False)
        print(self.cleaned_data)
        instance.quarter = models.Quarters.get_quarter_by_date(
            self.cleaned_data['date'])
        instance.group = kwargs['group']
        if self.cleaned_data['deleteFile']:
            instance.h_file = None
        if commit:
            instance.save()
        return instance


class QuarterSelectionForm(forms.Form):
    quarter = forms.ChoiceField(
        label="Четверть",
        choices=QUARTERS,
    )


class VisibleStudentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = self.instance.klass.students_set.all()

    class Meta:
        model = models.Groups
        fields = ['students']
        widgets = {
            "students": forms.CheckboxSelectMultiple()
        }


class GroupSelectionForm(forms.Form):
    classes = forms.ModelChoiceField(
        models.Klasses.objects.all(), label="Класс")
    subjects = forms.ModelChoiceField(
        models.Subjects.objects.all(), label="Предмет")
    quarters = forms.ChoiceField(choices=QUARTERS, label="Четверть")

    def __init__(self, *args, subjects=None, classes=None, **kwargs):
        super().__init__(*args, **kwargs)
        if subjects:
            self.fields['subjects'].queryset = subjects
            self.fields['subjects'].initial = subjects[0]
        if classes:
            self.fields['classes'].queryset = classes
            self.fields['classes'].initial = classes[0]

    def clean_quarters(self):
        return int(self.cleaned_data['quarters'])

    def get_group(self):
        group, created = models.Groups.objects.get_or_create(
            klass=self.cleaned_data['classes'],
            subject=self.cleaned_data['subjects']
        )
        if created:
            group.set_default_students()
        return group

from django import forms
from . import models
from . import functions
import utils


bts4attr = {'class': 'form-control'}
custom_select = {'class': 'custom-select'}
bts4attr_file = {'class': 'custom-file-input'}
QUARTERS = [(1, "I"), (2, "II"), (3, "III"), (4, "IV")]


class DatePickForm(forms.Form):
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date',
    }))


class LessonCreationForm(forms.ModelForm):
    """Form for creating/editing a lesson."""
    class Meta:
        model = models.Lessons
        fields = (
            'date', 'theme', 'homework', 'h_file', 'control',
        )
        widgets = {
            'h_file': forms.FileInput(attrs=bts4attr_file),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'theme': forms.TextInput(attrs=bts4attr),
            'homework': forms.Textarea(attrs=bts4attr),
            'control': forms.Select(attrs=bts4attr),
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
        if not functions.get_quarter_by_date(str(date)):
            self.fields['date'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def save(self, commit=True, **kwargs):
        instance = super(LessonCreationForm, self).save(commit=False)
        instance.quarter = functions.get_quarter_by_date(str(self.cleaned_data['date']))
        instance.group = kwargs['group']
        if kwargs.get('deletefile'):
            instance.h_file = None
        if commit:
            instance.save()
        return instance


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = models.Lessons
        fields = ('homework', 'h_file', 'date')
        labels = {
            'h_file': 'Файл с домашним заданием',
            'homework': 'Домашнее задание на создаваемый урок',
            'date': 'Дата'
        }
        widgets = {
            'h_file': forms.FileInput(attrs={
                'class': 'custom-file-input', 'id': 'f_file'
            }),
            'homework': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'f_hw'
            }),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'class': 'form-control', 'type': 'date', 'id': 'f_date'
            }),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if not functions.get_quarter_by_date(str(date)):
            self.fields['date'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def add_homework(self, group: int) -> models.Lessons:
        """
        Add homework to specified date.

        Args:
            group - current id of diary.models.Groups
        """
        date = self.cleaned_data.get('date')
        quarter: int = utils.get_quarter_by_date(date)
        homework: str = self.cleaned_data.get('homework', '')
        h_file = self.cleaned_data.get('h_file')
        if quarter == 0:
            raise ValueError("Lesson's date can't be on holidays.")
        lessons = models.Lessons.objects.filter(
            group_id=group,
            date=date
            )
        for lesson in lessons:
            if not (lesson.homework or lesson.h_file):
                lesson.homework = homework
                lesson.h_file = h_file
                lesson.save()
                return lesson
        # Lesson with no homework wasn't found, so we are
        # going to create a new one.
        control = models.Controls.objects.get_or_create(
            name="Работа на уроке", weight=1
        )[0]
        lesson = models.Lessons.objects.create(
            date=date, quarter=quarter,
            homework=self.cleaned_data.get('homework', ''),
            h_file=self.cleaned_data.get('h_file'),
            control=control, group_id=group
        )
        return lesson


class QuarterSelectionForm(forms.Form):
    quarter = forms.ChoiceField(
        label="Четверть",
        choices=QUARTERS,
        widget=forms.Select(attrs=bts4attr)
    )


class VisibleStudentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = self.instance.grade.students_set.all()

    class Meta:
        model = models.Groups
        fields = ['students']
        widgets = {
            "students": forms.CheckboxSelectMultiple(attrs={"class": "check-input"})
        }


class GroupSelectionForm(forms.Form):
    classes = forms.ModelChoiceField(
        models.Grades.objects.all(),
        label="Класс",
        widget=forms.Select(attrs=custom_select))
    subjects = forms.ModelChoiceField(
        models.Subjects.objects.all(),
        label="Предмет",
        widget=forms.Select(attrs=custom_select))
    quarters = forms.ChoiceField(
        choices=QUARTERS,
        label="Четверть",
        widget=forms.Select(attrs=custom_select))

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
            grade=self.cleaned_data['classes'],
            subject=self.cleaned_data['subjects']
        )
        if created:
            group.set_default_students()
        return group

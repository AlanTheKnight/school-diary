from django import forms
from core import models
from .homework import add_homework
from diary import functions
import utils


# 20 Mb
MAX_FILE_SIZE = 20


class PresidentHomeworkForm(forms.ModelForm):
    """
    Form that allows students with ``president`` status
    add homework for their class.
    """
    subject = forms.ModelChoiceField(
        queryset=models.Subjects.objects.all(), label="Предмет",
        widget=forms.Select(
            attrs={'class': 'form-control'}),
        )

    class Meta:
        model = models.Lessons
        fields = ('homework', 'h_file', 'date', 'subject')
        labels = {
            'h_file': 'Файл с домашним заданием',
            'homework': 'Домашнее задание на создаваемый урок',
            'date': 'Дата'
        }
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': 'date'
            }),
            'h_file': forms.FileInput()
        }

    def __init__(self, subjects, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = subjects
        if self.instance.id is not None:
            self.fields['subject'].initial = self.instance.group.subject

    def clean_date(self):
        date = self.cleaned_data['date']
        if not functions.get_quarter_by_date(str(date)):
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def clean_h_file(self):
        content = self.cleaned_data['h_file']
        if content is not None:
            if content.size > MAX_FILE_SIZE * 1024 * 1024:
                current_size = round(content.size / 1024 / 1024, 1)
                raise forms.ValidationError(
                    "Размер файла не должен превышать %s Мб. Текущий размер: %s Мб" % (
                        MAX_FILE_SIZE, current_size)
                )
        return content

    def clean(self):
        super().clean()
        if self.cleaned_data['h_file'] is None and not self.cleaned_data['homework']:
            raise forms.ValidationError("Укажите задание или прикрепите файл")

    def add_homework(self, klass) -> models.Lessons:
        subject = self.cleaned_data.pop('subject')
        group = utils.get_group(subject, klass)
        add_homework(**self.cleaned_data, group=group)

    def save(self):
        data: models.Lessons = super().save(commit=False)
        group = utils.get_group(
            self.cleaned_data['subject'], self.instance.group.klass)
        data.group = group
        if not self.data.get("deleteFile") is None:
            data.h_file.delete()
        data.save()
        return data


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
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': 'date'
            }),
            'h_file': forms.FileInput()
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if not models.Quarters.get_quarter_by_date(str(date)):
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def clean_h_file(self):
        content = self.cleaned_data['h_file']
        if content is not None:
            if content.size > MAX_FILE_SIZE * 1024 * 1024:
                current_size = round(content.size / 1024 / 1024, 1)
                raise forms.ValidationError(
                    "Размер файла не должен превышать %s Мб. Текущий размер: %s Мб" % (
                        MAX_FILE_SIZE, current_size)
                )
        return content

    def clean(self):
        super().clean()
        if self.cleaned_data['h_file'] is None and not self.cleaned_data['homework']:
            raise forms.ValidationError("Укажите задание или прикрепите файл")

    def add_homework(self, group: models.Groups) -> models.Lessons:
        add_homework(**self.cleaned_data, group=group)

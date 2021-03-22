from django import forms

import utils
from apps.core import models
from apps.diary import functions

# 20 Mb
MAX_FILE_SIZE = 20


class BaseHomeworkForm(forms.ModelForm):
    date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = models.Homework
        fields = ('date', 'content', 'h_file')
        labels = {
            'h_file': 'Файл с домашним заданием',
            'content': 'Домашнее задание',
        }

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

    def clean_date(self):
        date = self.cleaned_data['date']
        if not functions.get_quarter_by_date(str(date)):
            raise forms.ValidationError("Урок не может быть на каникулах")
        return date

    def clean(self):
        super().clean()
        if self.cleaned_data['h_file'] is None and not self.cleaned_data['content']:
            raise forms.ValidationError("Укажите задание или прикрепите файл")


class PresidentHomeworkForm(BaseHomeworkForm):
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
        model = models.Homework
        fields = ('date', 'subject', 'content', 'h_file')
        labels = {
            'h_file': 'Файл с домашним заданием',
            'content': 'Домашнее задание',
        }

    def __init__(self, subjects=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id is not None:
            self.fields['subject'].queryset = self.instance.lesson.group.klass.subjects.all()
            self.fields['subject'].initial = self.instance.lesson.group.subject
            self.fields['date'].initial = self.instance.lesson.date
        else:
            self.fields['subject'].queryset = subjects

    def add_homework(self, klass: models.Klasses) -> models.Homework:
        subject = self.cleaned_data.pop('subject')
        group = utils.get_group(subject, klass)
        return models.Homework.add_homework(group=group, **self.cleaned_data)

    def save(self, commit=True) -> models.Homework:
        data: models.Homework = super().save(commit=False)
        group = utils.get_group(self.cleaned_data.pop('subject'), self.instance.lesson.group.klass)
        if data.lesson.date != self.cleaned_data['date']:
            data.delete()
            return models.Homework.add_homework(**self.cleaned_data, group=group)
        data.group = group
        if not self.data.get("deleteFile") is None:
            data.h_file.delete()
        data.save()
        return data


class HomeworkForm(BaseHomeworkForm):
    class Meta:
        model = models.Homework
        fields = ('content', 'h_file', 'date')
        labels = {
            'h_file': 'Файл с домашним заданием',
            'content': 'Домашнее задание на создаваемый урок',
            'date': 'Дата'
        }

    def add_homework(self, group: models.Groups) -> models.Homework:
        return models.Homework.add_homework(group=group, **self.cleaned_data)

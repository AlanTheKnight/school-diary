from django import forms
from diary import models
from diary import functions
import utils


# 20 Mb
MAX_FILE_SIZE = 20


class HomeworkForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=models.Subjects.objects.all(), label="Предмет",
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'f_subject'}),
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
            'h_file': forms.FileInput(attrs={
                'id': 'f_file'
            }),
            'homework': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'f_hw'
            }),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'class': 'form-control', 'type': 'date'
            }),
        }

    def __init__(self, subjects, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = subjects
        if self.instance.id is not None:
            self.fields['subject'].initial = self.instance.group.subject

    def clean_date(self):
        date = self.cleaned_data['date']
        if not functions.get_quarter_by_date(str(date)):
            self.fields['date'].widget.attrs['class'] += ' is-invalid'
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

    def add_homework(self, grade: models.Grades) -> models.Lessons:
        """
        Add homework to specified date.

        Args:
            group - current id of diary.models.Groups
        """
        subject = self.cleaned_data.get('subject')
        group = utils.get_group(subject, grade)
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
            control=control, group=group
        )
        return lesson

    def save(self):
        data: models.Lessons = super().save(commit=False)
        group = utils.get_group(
            self.cleaned_data['subject'], self.instance.group.grade)
        data.group = group
        data.save()
        return data

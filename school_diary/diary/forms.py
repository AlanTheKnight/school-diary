from django import forms
from . import models
from . import functions


bts4attr = {'class': 'form-control'}
bts4attr_file = {'class': 'custom-file-input'}


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
            'date': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'theme': forms.TextInput(attrs=bts4attr),
            'homework': forms.Textarea(attrs=bts4attr),
            'control': forms.Select(attrs=bts4attr),
        }
        labels = {
            'h_file': 'Файл с домашним заданием',
            'date': 'Дата',
            'theme': 'Тема урока',
            'homework': 'Домашнее задание',
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
        instance.subject = kwargs['subject']
        instance.grade = kwargs['grade']
        if kwargs.get('deletefile'):
            instance.h_file = None
        if commit:
            instance.save()
        return instance


class QuarterSelectionForm(forms.Form):
    quarter = forms.ChoiceField(
        label="Четверть",
        choices=[(1, "I"), (2, "II"), (3, "III"), (4, "IV")],
        widget=forms.Select(attrs=bts4attr)
    )

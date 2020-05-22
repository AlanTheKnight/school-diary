from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from . import models
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from . import functions


bts4attr = {'class': 'form-control'}
bts4attr_file = {'class': 'custom-file-input'}


class UsersLogin(forms.Form):
    email = forms.EmailField(
        label="Электронная почта: ", max_length=50, widget=forms.EmailInput(attrs=bts4attr))
    password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput(attrs=bts4attr))


class StudentSignUpForm(UserCreationForm):
    """
    Form for student sign up. When saved, set user account type
    to 3 and add user to students group.
    """
    first_name = forms.CharField(
        label="Имя", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    surname = forms.CharField(
        label="Фамилия", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    second_name = forms.CharField(
        label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs=bts4attr))
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={
                'class': 'form-control', 'autocomplete': 'new-password',
                'id': "password1", 'name': 'password1'
            }))
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'autocomplete': 'new-password', "id": "password2"
        }))

    class Meta():
        model = models.Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'myemail@example.com', "id": "email"
                }),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 3
        user.is_superuser = False
        user.is_staff = False
        try:
            user_group = Group.objects.get(name='students')
        except ObjectDoesNotExist:
            user_group = Group.objects.create(name='students')
            user_group.save()
        user.save()
        user.groups.add(user_group)
        user.save()
        models.Students.objects.create(
            account=user,
            first_name=self.cleaned_data['first_name'],
            surname=self.cleaned_data['surname'],
            second_name=self.cleaned_data['second_name']
        )
        return user


class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    surname = forms.CharField(
        label="Фамилия", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    second_name = forms.CharField(
        label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs=bts4attr))
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={
                'class': 'form-control', 'autocomplete': 'new-password',
                'id': "password1", 'name': 'password1'
            }))
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'autocomplete': 'new-password', "id": "password2"}))

    class Meta():
        model = models.Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={
                    'class': 'form-control', 'placeholder': 'myemail@example.com', "id": "email"
                }),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 1
        user.is_superuser = False
        user.is_staff = True
        user.save()
        try:
            user_group = Group.objects.get(name='admins')
        except ObjectDoesNotExist:
            user_group = Group.objects.create(name='admins')
        user.save()
        user.groups.add(user_group)
        models.Administrators.objects.create(
            account=user,
            first_name=self.cleaned_data['first_name'],
            surname=self.cleaned_data['surname'],
            second_name=self.cleaned_data['second_name'],)
        return user


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    surname = forms.CharField(
        label="Фамилия", max_length=100, widget=forms.TextInput(attrs=bts4attr))
    second_name = forms.CharField(
        label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs=bts4attr))
    subjects = forms.ModelMultipleChoiceField(
        queryset=models.Subjects.objects.all(), widget=forms.SelectMultiple(attrs=bts4attr))
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={
                'class': 'form-control', 'autocomplete': 'new-password',
                'id': "password1", 'name': 'password1'
            }))
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput(attrs={
                'class': 'form-control', 'autocomplete': 'new-password', "id": "password2"
            }))

    class Meta():
        model = models.Users
        fields = (
            'email', 'first_name', 'surname',
            'second_name', 'subjects', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={
                    'class': 'form-control', 'placeholder': 'myemail@example.com'
                }),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 2
        user.is_superuser = False
        user.is_staff = False
        user.save()
        try:
            user_group = Group.objects.get(name='teachers')
        except ObjectDoesNotExist:
            user_group = Group.objects.create(name='teachers')
        user.save()
        user.groups.add(user_group)
        admin = models.Teachers.objects.create(
            account=user,
            first_name=self.cleaned_data['first_name'],
            surname=self.cleaned_data['surname'],
            second_name=self.cleaned_data['second_name'],)
        admin.subjects.set(self.cleaned_data['subjects'])
        return user


class AddStudentToGradeForm(forms.Form):
    email = forms.CharField(
        label="Почта", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))
    first_name = forms.CharField(
        label="Имя", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))
    surname = forms.CharField(
        label="Фамилия", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))


class GradeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Grades
        fields = ('number', 'letter', 'subjects', 'teachers')
        widgets = {
            'number': forms.Select(attrs=bts4attr),
            'letter': forms.Select(attrs=bts4attr),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'subjects'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'teachers'}),
        }


class AdminMessageCreationForm(forms.ModelForm):
    class Meta:
        model = models.AdminMessages
        fields = ('subject', 'content')
        widgets = {
            'subject': forms.TextInput(attrs=bts4attr),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
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


class DatePickForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date', 'id': 'date'
    }))


class CreateSubjectForm(forms.Form):
    class Meta:
        model = models.Subjects


class ClassSettingsForm(forms.ModelForm):
    class Meta:
        model = models.Grades
        fields = ('subjects', 'teachers')
        widgets = {
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'subjects'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'teachers'}),
        }


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
                'data-toggle': 'datepicker',
                'autocomplete': 'off',
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
        self.fields['date'].widget.attrs['class'] += ' is-invalid'
        if not functions.get_quarter_by_date(str(date)):
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

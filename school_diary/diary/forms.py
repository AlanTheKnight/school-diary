from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import request
from .models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist


class UsersLogin(forms.Form):
    email = forms.EmailField(label="Электронная почта: ", max_length=50, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput(attrs={'class':'form-control'}))


class StudentSignUpForm(UserCreationForm):
    """
    Form for student sign up. When saved, set user account type to 3 and add user to students group.
    """
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    second_name = forms.CharField(label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password', 'pattern':r"(?=.*\d)(?=.*[a-zA-Z]).{8,}", 'id':"password1", 'name':'password1'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))

    class Meta():
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'myemail@example.com'}),
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
        student = Students.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        return user


class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    second_name = forms.CharField(label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password', 'pattern':r"(?=.*\d)(?=.*[a-zA-Z]).{8,}", 'id':"password1", 'name':'password1'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))

    class Meta():
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'myemail@example.com'}),
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
        admin = Administrators.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        return user


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    second_name = forms.CharField(label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password', 'pattern':r"(?=.*\d)(?=.*[a-zA-Z]).{8,}", 'id':"password1", 'name':'password1'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))

    class Meta():
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'subjects', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'myemail@example.com'}),
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
        admin = Teachers.objects.create(account=user,
                                        first_name=self.cleaned_data['first_name'],
                                        surname=self.cleaned_data['surname'],
                                        second_name=self.cleaned_data['second_name'],)
        admin.subjects.set(self.cleaned_data['subjects'])
        return user


class AddStudentToGradeForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class GradeCreationForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ('number', 'letter', 'subjects', 'teachers')
        widgets = {
            'number':forms.Select(attrs={'class': 'form-control'}),
            'letter':forms.Select(attrs={'class': 'form-control'}),
            'subjects':forms.SelectMultiple(attrs={'class': 'form-control'}),
            'teachers':forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class AdminMessageCreationForm(forms.ModelForm):
    class Meta:
        model = AdminMessages
        fields = ('subject', 'content')
        widgets = {
            'subject':forms.TextInput(attrs={'class': 'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('first_name', 'surname', 'second_name', 'grade')
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'surname':forms.TextInput(attrs={'class': 'form-control'}),
            'second_name':forms.TextInput(attrs={'class': 'form-control'}),
            'grade':forms.Select(attrs={'class': 'form-control'}),
        }


class AdminsEditForm(forms.ModelForm):
    class Meta:
        model = Administrators
        fields = ('first_name', 'surname', 'second_name')
        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'surname':forms.TextInput(attrs={'class': 'form-control'}),
            'second_name':forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ('first_name', 'surname', 'second_name', 'subjects')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class LessonCreationForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ('subject', 'grade', 'date', 'theme', 'homework', 'control')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', }),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import request

from .models import Users, Students, Administrators, Teachers, Grades, Subjects
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist



# class StudentRegistration(forms.Form):
#     email = forms.EmailField(label="Электронная почта: ", max_length=50)
#     first_name = forms.CharField(label="Имя: ", max_length=50)
#     surname = forms.CharField(label="Фамилия: ", max_length=50)
#     password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput)
#     conform_password = forms.CharField(label="Подтверждение пароля: ", widget=forms.PasswordInput)
#     grade = forms.ChoiceField(label="Класс:", choices=[
#         (1, 1),
#         (2, 2),
#         (3, 3),
#         (4, 4),
#         (5, 5),
#         (6, 6),
#         (7, 7),
#         (8, 8),
#         (9, 9),
#         (10, 10),
#         (11, 11)])
#     litera = forms.ChoiceField(label="Литера:", choices=[
#         ("А", "А"),
#         ("Б", "Б"),
#         ("В", "В"),
#         ("Г", "Г"),
#         ("Д", "Д"),
#         ("Е", "Е"),
#         ("Ж", "Ж"),
#         ("З", "З")])


# class StudentCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Students
#         fields = ('email', 'first_name', 'surname', 'second_name', 'grade')


# SUBJECTS = list()


class UsersLogin(forms.Form):
    email = forms.EmailField(label="Электронная почта: ", max_length=50)
    password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput)


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    second_name = forms.CharField(label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))
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
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))
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
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    surname = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    second_name = forms.CharField(label="Отчество", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}))

    class Meta():
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'subjects', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'myemail@example.com'}),
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




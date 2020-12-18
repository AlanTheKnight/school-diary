from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from diary import models


bts4attr = {'class': 'form-control'}
bts4attr_file = {'class': 'custom-file-input'}


class UsersLogin(forms.Form):
    email = forms.EmailField(
        label="Электронная почта", max_length=50, widget=forms.EmailInput(attrs=bts4attr))
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs=bts4attr))


class StudentSignUpForm(UserCreationForm):
    """
    Form for student sign up. When saved, set user account type
    to 3 and add user to students group.
    """
    first_name = forms.CharField(
        label="Имя", max_length=50)
    surname = forms.CharField(
        label="Фамилия", max_length=100)
    second_name = forms.CharField(
        label="Отчество", max_length=100, required=False)

    class Meta:
        model = models.Users
        fields = "__all__"
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'myemail@example.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
            }),
            'password2': forms.PasswordInput(attrs={
                'autocomplete': 'new-password'
            })
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
        fields = ('email', 'first_name', 'surname',
                  'second_name', 'password1', 'password2')
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
        user_group = Group.objects.get_or_create(name='admins')[0]
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
        user_group = Group.objects.get_or_create(name='teachers')[0]
        user.save()
        user.groups.add(user_group)
        admin = models.Teachers.objects.create(
            account=user,
            first_name=self.cleaned_data['first_name'],
            surname=self.cleaned_data['surname'],
            second_name=self.cleaned_data['second_name'],)
        admin.subjects.set(self.cleaned_data['subjects'])
        return user


class AdminMessageCreationForm(forms.ModelForm):
    class Meta:
        model = models.AdminMessages
        fields = ('subject', 'content')
        widgets = {
            'subject': forms.TextInput(attrs=bts4attr),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

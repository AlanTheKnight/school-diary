from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Users, Students, Administrators, Teachers, Grades, Subjects
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist


class UserLogin(forms.Form):
    email = forms.EmailField(label="Электронная почта: ", max_length=50)
    password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput)


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100)
    surname = forms.CharField(label="Фамилия", max_length=100)
    second_name = forms.CharField(label="Отчество", max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name')

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
        user.groups.add(user_group)
        user.save()
        student = Students.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        return user


class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100)
    surname = forms.CharField(label="Фамилия", max_length=100)
    second_name = forms.CharField(label="Отчество", max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name')

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
        user.groups.add(user_group)
        admin = Administrators.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        return user


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100)
    surname = forms.CharField(label="Фамилия", max_length=100)
    second_name = forms.CharField(label="Отчество", max_length=100, required=False)
    subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all())

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('email', 'first_name', 'surname', 'second_name', 'subjects')

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
        user.groups.add(user_group)
        admin = Teachers.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        admin.subjects.set(self.cleaned_data['subjects'])
        return user

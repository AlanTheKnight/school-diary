from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Users, Students, Administrators, Teachers, Grades, Subjects


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
        admin = Teachers.objects.create(account=user,
                                          first_name=self.cleaned_data['first_name'],
                                          surname=self.cleaned_data['surname'],
                                          second_name=self.cleaned_data['second_name'],)
        admin.subjects.set(self.cleaned_data['subjects'])
        return user

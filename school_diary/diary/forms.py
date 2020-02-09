from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Users, Students


class StudentsLogin(forms.Form):
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

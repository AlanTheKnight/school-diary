from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.core import models

form_fields = (
    "first_name", "second_name", "surname",
    "email", "password1", "password2"
)


class UsersLogin(forms.Form):
    email = forms.EmailField(
        label="Электронная почта", max_length=50)
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput())


class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = models.Users
        fields = form_fields
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'myemail@example.com'
            })
        }
        help_texts = {
            "password1": "Не используйте часто встречающиеся пароли"
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 3
        user.is_superuser = False
        user.is_staff = False
        user.save()
        user.add_to_group()
        user.save()
        models.Students.objects.create(account=user)
        return user


class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = models.Users
        fields = form_fields
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'myemail@example.com'
            })
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 1
        user.is_superuser = False
        user.is_staff = True
        user.save()
        user.add_to_group()
        user.save()
        user.create_account()
        return user


class TeacherSignUpForm(UserCreationForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=models.Subjects.objects.all(),
        label="Предметы",
        required=False,
        help_text=(
                "Удерживайте “Control“ (или “Command“ на Mac)," +
                "чтобы выбрать несколько значений.")
    )

    class Meta:
        model = models.Users
        fields = form_fields + ("subjects",)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'myemail@example.com'
            }),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.account_type = 2
        user.is_superuser = False
        user.is_staff = False
        user.save()
        user.add_to_group()
        user.save()
        t = models.Teachers.objects.create(account=user)
        t.subjects.set(self.cleaned_data['subjects'])
        t.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.Users
        fields = [
            "email", "first_name",
            "second_name", "surname"
        ]


class StudentEditForm(UserEditForm):
    klass = forms.ModelChoiceField(
        queryset=models.Klasses.objects.all(), label="Класс", required=False)

    def save(self, *args, **kwargs):
        u = super().save(commit=False)
        u.student.klass = self.cleaned_data['klass']
        u.student.save()
        return u

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['klass'].initial = self.instance.student.klass


class TeacherEditForm(UserEditForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=models.Subjects.objects.all(),
        label="Предметы",
        required=False,
        help_text=(
                "Удерживайте “Control“ (или “Command“ на Mac)," +
                "чтобы выбрать несколько значений.")
    )

    def save(self, *args, **kwargs):
        u = super().save(commit=False)
        u.teacher.subjects.set(self.cleaned_data['subjects'])
        u.teacher.save()
        return u

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['subjects'].initial = self.instance.teacher.subjects.all()


class MessageToAdminForm(forms.ModelForm):
    class Meta:
        model = models.AdminMessages
        fields = ('subject', 'content')

    def save(self, commit=True, sender=None):
        if sender is None:
            raise ValueError("Message sender must be specified.")
        message = super(MessageToAdminForm, self).save(commit=False)
        message.sender = sender
        message.save()
        return message

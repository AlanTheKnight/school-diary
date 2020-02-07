from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.db import models
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


TYPES = [
	(0, "Root"),
	(1, "Администратор"),
	(2, "Учитель"),
	(3, "Ученик"),
]


class Users(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('Почта', unique=True)
	account_type = models.IntegerField(verbose_name="Тип аккаунта", default=3)
	is_active = models.BooleanField('Активный', default=True)
	is_staff = models.BooleanField('Администратор', default=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['account_type']

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def get_username(self):
		return self.email

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)


class Students(models.Model):
	account = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="Пользователь")
	first_name = models.CharField(verbose_name="Имя", max_length=100)
	surname = models.CharField(verbose_name="Фамилия", max_length=100)
	second_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True)
	# grade = models.ForeignKey(Grades, on_delete=models.SET_NULL, null=True, default=None, verbose_name="Класс")
	# TODO: Сделать модель класса

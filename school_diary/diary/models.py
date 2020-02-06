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
	account_type = models.IntegerField(verbose_name="Тип аккаунта", choices=TYPES, default=3)
	date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
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
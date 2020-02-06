from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.db import models
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('email address', unique=True)
	first_name = models.CharField('first name', max_length=30, blank=True)
	last_name = models.CharField('last name', max_length=30, blank=True)
	date_joined = models.DateTimeField('date joined', auto_now_add=True)
	is_active = models.BooleanField('active', default=True)
	is_staff = models.BooleanField('active', default=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def get_full_name(self):
		'''
		Returns the first_name plus the last_name, with a space in between.
		'''
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
		Returns the short name for the user.
		'''
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		'''
		Sends an email to this User.
		'''
		send_mail(subject, message, from_email, [self.email], **kwargs)
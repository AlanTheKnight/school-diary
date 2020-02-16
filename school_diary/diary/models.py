from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from .managers import UserManager

TYPES = [
    (0, "Root"),
    (1, "Администратор"),
    (2, "Учитель"),
    (3, "Ученик"),
]


GRADES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11)
]

LITERAS = [
    ("А", "А"),
    ("Б", "Б"),
    ("В", "В"),
    ("Г", "Г"),
    ("Д", "Д"),
    ("Е", "Е"),
    ("Ж", "Ж"),
    ("З", "З"),
    ("И", "И"),
    ("К", "К")
]


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    account_type = models.IntegerField(verbose_name="Тип аккаунта", default=3, choices=TYPES)
    is_active = models.BooleanField('Активный', default=True)
    is_staff = models.BooleanField('Администратор', default=False)

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


class Subjects(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Teachers(models.Model):
    account = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="Пользователь", primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    second_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True)
    subjects = models.ManyToManyField(Subjects, verbose_name="Предметы")

    class Meta:
        ordering = ['surname', 'first_name', 'second_name']
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    def __str__(self):
        return '{} {} {}'.format(self.surname, self.first_name, self.second_name)


class Grades(models.Model):
    number = models.IntegerField(choices=GRADES, verbose_name="Класс")
    letter = models.CharField(max_length=2, choices=LITERAS, verbose_name="Буква")
    teachers = models.ManyToManyField(Teachers, verbose_name="Учителя", related_name="subjects_chosen")
    subjects = models.ManyToManyField(Subjects, verbose_name="Предметы")
    main_teacher = models.ForeignKey(Teachers, verbose_name='Классный руководитель', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        ordering = ['number', 'letter']
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return '{}{}'.format(self.number, self.letter)


class Students(models.Model):
    account = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="Пользователь", primary_key=True)
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)
    second_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True, default="")
    grade = models.ForeignKey(Grades, on_delete=models.SET_NULL, null=True, default=None, verbose_name="Класс",
                              blank=True)

    class Meta:
        ordering = ['grade', 'surname', 'first_name', 'second_name']
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return '{} {} {} {}'.format(self.first_name, self.second_name, self.surname, self.grade)


class Administrators(models.Model):
    account = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="Пользователь", primary_key=True)
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)
    second_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return '{} {} {}'.format(self.surname, self.first_name, self.second_name)


class Lessons(models.Model):
    date = models.DateField(verbose_name='Дата')
    number = models.IntegerField(verbose_name='Номер урока')
    homework = models.TextField(blank=True, verbose_name='ДЗ')
    Theme = models.CharField(max_length=120, verbose_name='Тема')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Предмет')
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name='Класс')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return '{} {} {}'.format(self.subject, self.grade, self.date)
# TODO Weights system


class Marks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="Ученик")
    amount = models.IntegerField(verbose_name="Балл")
    date = models.DateField(verbose_name="Дата")
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, verbose_name='Урок', default='')

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['date', 'amount']

    def __str__(self):
        return '"{}" {} {}'.format(self.amount, self.lesson, self.student)


class AdminMessages(models.Model):
    date = models.DateTimeField(verbose_name="Время отправки", auto_now_add=True)
    subject = models.CharField(verbose_name="Тема сообщения", max_length=100)
    content = models.TextField(verbose_name="Текст сообщения", max_length=4000)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Отправитель", null=True, default=None)
    
    class Meta:
        verbose_name = "Сообщение администратору"
        verbose_name_plural = "Сообщения администратору"
        ordering = ['date', 'subject']

    def __str__(self):
        return self.subject
        
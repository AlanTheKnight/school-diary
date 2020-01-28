from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import date


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
    ("З", "З")
]


MARKS = [
    (5, "5 - отлично"),
    (4, "4 - хорошо"),
    (3, "3 - удовлетворительно"),
    (2, "2 - плохо"),
    (1, "1 - ужасно")
]

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class Subjects(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        ordering = ['name']
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Teachers(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    second_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    subjects = models.ManyToManyField(Subjects, verbose_name="Предметы")
    password = models.CharField(max_length=50, verbose_name="Пароль")
    email = models.EmailField(max_length=50, verbose_name="Почта", default='test')
    active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'surname', ]

    class Meta:
        ordering = ['surname', 'first_name', 'second_name']
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    def __str__(self):
        return '{} {} {}'.format(self.surname, self.first_name, self.second_name)


class Grades(models.Model):
    number = models.IntegerField(choices=GRADES, verbose_name="Класс")
    letter = models.CharField(max_length=2, verbose_name="Буква")
    main_teacher = models.ForeignKey(Teachers, null=True, on_delete=models.SET_NULL, verbose_name="Классный руководитель")

    class Meta:
        ordering = ['number', 'letter']
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return '{}{}'.format(self.number, self.letter)


class Students(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    second_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    password = models.CharField(max_length=50, verbose_name="Пароль")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="Класс")
    email = models.EmailField(max_length=50, verbose_name="Почта", default='test', unique=True)
    active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'surname',  'grade']

    objects = CustomUserManager()

    def get_username(self):
        return self.email

    class Meta:
        ordering = ['surname', 'first_name', 'second_name']
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return '{} {} {}'.format(self.surname, self.first_name, self.second_name)


class HomeTasks(models.Model):
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="Класс")
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name="Предмет")
    description = models.CharField(max_length=1000, verbose_name="Описание домашнего задания")
    creation_date = models.DateField(verbose_name="Когда задано", default=date.today)
    day_to_make = models.DateField(verbose_name="На какой день задано")

    class Meta:
        ordering = ['day_to_make']
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"

    def __str__(self):
        return "Д/з на {}".format(self.day_to_make)


class Marks(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name="Предмет")
    creation_date = models.DateField(default=date.today, verbose_name="Дата")
    mark = models.IntegerField(choices=MARKS, verbose_name="оценка", default=5)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="Ученик")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="Класс")
    comment = models.CharField(max_length=150, verbose_name="Комментарий", blank=True)

    class Meta:
        ordering = ['creation_date']
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return "{}: оценка {} за {}".format(self.student, self.mark, self.creation_date)


class Administration(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    second_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    password = models.CharField(max_length=50, verbose_name="Пароль")
    email = models.EmailField(max_length=50, verbose_name="Почта", default='test')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'surname', ]
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email


    class Meta:
        ordering = ['surname', 'first_name', 'second_name']
        verbose_name = "администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return '{} {} {}'.format(self.surname, self.first_name, self.second_name)
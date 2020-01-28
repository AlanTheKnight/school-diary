from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
#
# GRADES = [
#     (1, 1),
#     (2, 2),
#     (3, 3),
#     (4, 4),
#     (5, 5),
#     (6, 6),
#     (7, 7),
#     (8, 8),
#     (9, 9),
#     (10, 10),
#     (11, 11)
# ]
#
#
# LITERAS = [
#     ("А", "А"),
#     ("Б", "Б"),
#     ("В", "В"),
#     ("Г", "Г"),
#     ("Д", "Д"),
#     ("Е", "Е"),
#     ("Ж", "Ж"),
#     ("З", "З")
# ]
#
# class Subjects(models.Model):
#     name = models.CharField(max_length=50, verbose_name="Название")
#
#     class Meta:
#         ordering = ['name']
#         verbose_name = "Предмет"
#         verbose_name_plural = "Предметы"
#
#     def __str__(self):
#         return self.name
#
# # Create your models here.
#
#
# class Teachers(AbstractBaseUser):
#     first_name = models.CharField(max_length=50, verbose_name="Имя")
#     surname = models.CharField(max_length=50, verbose_name="Фамилия")
#     second_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
#     subjects = models.ManyToManyField(Subjects, verbose_name="Предметы")
#     login = models.CharField(max_length=50, verbose_name="Логин")
#     password = models.CharField(max_length=50, verbose_name="Пароль")
#
#     class Meta:
#         ordering = ['surname', 'first_name', 'second_name']
#         verbose_name = "Учитель"
#         verbose_name_plural = "Учителя"
#
#     def __str__(self):
#         return '{} {} {} '.format(self.surname, self.first_name, self.second_name)
#
#
# class Grades(models.Model):
#     number = models.IntegerField(choices=GRADES, verbose_name="Класс")
#     letter = models.CharField(max_length=2, verbose_name="Буква")
#     main_teacher = models.ForeignKey(Teachers, null=True, on_delete=models.SET_NULL, verbose_name="Классный руководитель")
#
#     class Meta:
#         ordering = ['number', 'letter']
#         verbose_name = "Класс"
#         verbose_name_plural = "Классы"
#
#     def __str__(self):
#         return str(self.number) + self.letter
#
#
# class Students(AbstractBaseUser):
#     first_name = models.CharField(max_length=50, verbose_name="Имя")
#     surname = models.CharField(max_length=50, verbose_name="Фамилия")
#     second_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
#     login = models.CharField(max_length=50, verbose_name="Логин")
#     password = models.CharField(max_length=50, verbose_name="Пароль")
#     grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="Класс")
#
#     class Meta:
#         ordering = ['surname', 'first_name', 'second_name']
#         verbose_name = "Учитель"
#         verbose_name_plural = "Учителя"
#
#     def __str__(self):
#         return self.surname + " " + self.first_name + " " + self.second_name



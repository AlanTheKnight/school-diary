from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

DAYS = [
    ("Понедельник", "Понедельник"),
    ("Вторник", "Вторник"),
    ("Среда", "Среда"),
    ("Четверг", "Четверг"),
    ("Пятница", "Пятница"),
    ("Суббота", "Суббота")
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


class Grades(models.Model):
    number = models.IntegerField(choices=GRADES, verbose_name="Класс")
    letter = models.CharField(max_length=1, choices=LITERAS, verbose_name="Литера")

    class Meta:
        ordering = ['number', 'letter']
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return str(self.number) + self.letter


class Lessons(models.Model):
    connection = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="У какого класса урок")
    day = models.CharField(max_length=11, choices=DAYS, verbose_name="День недели", blank=False)
    number = models.IntegerField(verbose_name="Номер урока", validators=[MinValueValidator(0), MaxValueValidator(8)])
    start = models.TimeField(verbose_name="Начало урока")
    end = models.TimeField(verbose_name="Конец урока")
    subject = models.CharField(max_length=50, verbose_name="Предмет")
    classroom = models.CharField(max_length=50 ,verbose_name="Кабинет")
    
    
    class Meta:
        ordering = ['connection', 'day', 'number']
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        if self.day != "Вторник":
            return str(self.number) + "й урок в " + self.day.lower() + " у " + str(self.connection)
        else:
            return str(self.number) + "й урок во " + self.day.lower() + " у " + str(self.connection)
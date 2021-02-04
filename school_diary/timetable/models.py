from django.db import models


DAYS = [
    ("Понедельник", "Понедельник"),
    ("Вторник", "Вторник"),
    ("Среда", "Среда"),
    ("Четверг", "Четверг"),
    ("Пятница", "Пятница"),
    ("Суббота", "Суббота")
]

SCHOOLS = [
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
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


class BellsTimeTable(models.Model):
    school = models.IntegerField(choices=SCHOOLS, verbose_name="Школа")
    n = models.IntegerField(verbose_name="Номер урока")
    start = models.TimeField(verbose_name="Начало урока")
    end = models.TimeField(verbose_name="Конец урока")

    class Meta:
        ordering = ['school', 'n']
        unique_together = ['school', 'n']
        verbose_name = "Звонок"
        verbose_name_plural = "Звонки"

    def __str__(self):
        return "Урок N{} - {}".format(self.n, dict(SCHOOLS)[self.school])


class Lessons(models.Model):
    klass = models.ForeignKey(
        "Klasses", default=None, on_delete=models.CASCADE, null=True,
        related_name="lessons", verbose_name="Класс")
    day = models.CharField(max_length=11, choices=DAYS, verbose_name="День недели", blank=False)
    number = models.ForeignKey(BellsTimeTable, on_delete=models.CASCADE, verbose_name="Номер урока")
    subject = models.CharField(max_length=50, verbose_name="Предмет")
    classroom = models.CharField(max_length=50, verbose_name="Кабинет")

    class Meta:
        ordering = ['klass', 'day', 'number']
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        if self.day != "Вторник":
            return str(self.number.n) + "й урок в " + self.day.lower() + " у " + str(self.connection)
        else:
            return str(self.number.n) + "й урок во " + self.day.lower() + " у " + str(self.connection)


class Klasses(models.Model):
    """
    Model that represents a grade in a timetable.

    Fields:
        id (PK), number (int), letter (str)
    """
    number = models.IntegerField(choices=GRADES, verbose_name="Класс")
    letter = models.CharField(max_length=2, choices=LITERAS, verbose_name="Буква")

    class Meta:
        ordering = ['number', 'letter']
        verbose_name = "Класс"
        verbose_name_plural = "Классы"
        unique_together = ('number', 'letter')

    def __str__(self):
        return '{}{}'.format(self.number, self.letter)

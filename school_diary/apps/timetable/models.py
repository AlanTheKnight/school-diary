from django.db import models
from apps.core.models import Subjects, Klasses


days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

SCHOOLS = [
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
]


LETTERS = [(i, i) for i in list("АБВГДЕЖЗИК")]
GRADES = [(i, i) for i in range(1, 12)]


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
        Klasses, default=None, on_delete=models.CASCADE, null=True,
        related_name="lessons", verbose_name="Класс")
    day = models.IntegerField(
        "День недели",
        choices=[(i+1, days[i]) for i in range(len(days))]
    )
    number = models.ForeignKey(BellsTimeTable, on_delete=models.CASCADE, verbose_name="Номер урока")
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name="Предмет")
    classroom = models.CharField(max_length=50, verbose_name="Кабинет")

    class Meta:
        ordering = ['klass', 'day', 'number']
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"Урок №{self.number.n} | {days[self.day]} | {self.klass}"

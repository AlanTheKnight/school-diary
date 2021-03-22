from django.db import models


SUBJECTS = [
    ("Информатика", "Информатика"),
    ("История", "История"),
    ("Литература", "Литература"),
    ("Математика", "Математика"),
    ("Обществознание", "Обществознание"),
    ("Русский язык", "Русский язык"),
    ("Химия и биология", "Хим-Био"),
    ("Экономика", "Экономика"),
    ("Физика", "Физика")
]

GRADES = [
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11)
]

TERMS = [
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV")
]


class Documents(models.Model):
    subject = models.CharField(max_length=20, choices=SUBJECTS, verbose_name="Предмет")
    grade = models.IntegerField(choices=GRADES, verbose_name="Класс")
    term = models.IntegerField(choices=TERMS, verbose_name="Четверть")
    file = models.FileField(upload_to='minimum/', verbose_name="Выберите файл")

    class Meta:
        ordering = ['subject', 'grade', 'term']
        verbose_name = "Минимум"
        verbose_name_plural = "Минимумы"

    def __str__(self):
        return (self.subject + " | " + str(self.grade) +
                " класс | " + str(self.term) + " четверть")

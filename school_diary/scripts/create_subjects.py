from diary import models


def run():
    while (name := input("> ")):
        m = models.Subjects.objects.create(name=name)
        m.save()

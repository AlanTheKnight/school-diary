from apps.core import models


def run():
    name: str
    while True:
        name = input("> ")
        if not name:
            break
        m = models.Subjects.objects.create(name=name)

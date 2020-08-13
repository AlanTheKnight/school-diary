from diary.models import Controls
from django.db.models.deletion import ProtectedError


def run():
    print("Getting the controls...")
    controls = Controls.objects.all()
    print("Listing them...\n")
    controls = Controls.objects.all()
    for i in range(len(controls)):
        print(i, controls[i])
    print("""Choose what controls do you want to delete.
Enter their numbers separated by space or 'ALL' to delete all of them.""")
    nums = input()
    if nums == "ALL":
        nums = list(range(len(controls)))
    else:
        nums = list(map(int, nums.split()))
    print("Deleting them...")
    for i in nums:
        try:
            controls[i].delete()
        except ProtectedError:
            print("Can't delete control {} because it's protected.".format(control))
    print("Creating new controls...")
    Controls.objects.create(name="Годовая оценка", weight=100)
    Controls.objects.create(name="Четвертная оценка", weight=100)
    Controls.objects.create(name="Контрольная работа", weight=5)
    Controls.objects.create(name="Проверочная работа", weight=4)
    Controls.objects.create(name="Самостоятельная работа", weight=3)
    Controls.objects.create(name="Домашняя работа", weight=2)
    Controls.objects.create(name="Работа на уроке", weight=1)
    print("Listing them...\n")
    controls = Controls.objects.all()
    for control in controls:
        print(control)
    print("\nDone.")

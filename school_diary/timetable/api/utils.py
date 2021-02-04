from timetable import models
import datetime


def generate_bell(n: int, num: int) -> tuple:
    generated: bool = False
    school: int = 1 if num < 5 else 2
    try:
        grade = models.BellsTimeTable.objects.get(n=n, school=school)
    except models.BellsTimeTable.DoesNotExist:
        start = datetime.datetime(2000, 1, 1, 9)  # 9:00
        le = datetime.timedelta(minutes=40)
        for i in range(1, n):
            start += le + datetime.timedelta(minutes=15)  # Break is 15 minutes
        end = start + le  # End of lesson
        grade = models.BellsTimeTable.objects.create(
            start=start.time(), end=end.time(), school=school, n=n)
        generated = True
    return (grade, generated)

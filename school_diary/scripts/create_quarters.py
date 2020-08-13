from diary.models import Quarters
from datetime import date


def run():
    year = int(input("Enter a year when 1st quarter begins > "))
    dates = ((1, 9, 27, 10), (3, 11, 29, 12), (12, 1, 21, 3), (29, 3, 27, 5))
    for i in range(0, 4):
        Quarters.objects.create(
            number=i+1, begin=date((year if i < 2 else year + 1), dates[i][1], dates[i][0]),
            end=date((year if i < 2 else year + 1), dates[i][3], dates[i][2]))

from django import template

register = template.Library()


@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]


@register.filter(name="smart_average")
def smartaverage(value):
    if value[1] != 0:
        return round(value[0] / value[1], 2)
    else:
        return "-"


@register.filter(name="average")
def average(value):
    if value[3] != 0:
        return round(value[2] / value[3], 2)
    else:
        return "-"


@register.filter(name='minus')
def minus(value, arg):
    return value - arg


@register.filter(name="grades_header")
def grades_header(lessons):
    result = []
    count = 1
    for i in range(1, len(lessons)):
        if lessons[i-1].date.month == lessons[i].date.month:
            count += 1
        else:
            result.append((lessons[i-1], count))
            count = 1
    result.append((lessons.last(), count))
    return result

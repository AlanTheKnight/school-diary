from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()


@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

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
    
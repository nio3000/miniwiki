from django import template

register = template.Library()

@register.filter
def cut(value, limit=100):
    return value[:100]

@register.filter
def formated_time(value):
    return value.strftime("%c")
from django.template.defaulttags import register
from django import template

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)
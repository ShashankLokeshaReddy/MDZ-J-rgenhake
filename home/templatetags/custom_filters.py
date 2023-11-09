# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='create_range')
def create_range(value):
    return range(value)

# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='create_range_masse')
def create_range_masse(value):
    return range(value)

@register.filter(name='create_range_schnittstellen')
def create_range_schnittstellen(value):
    return range(value)
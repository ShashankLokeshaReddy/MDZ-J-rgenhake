# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='create_range_masse')
def create_range_masse(value):
    return range(value)

@register.filter(name='create_range_schnittstellen')
def create_range_schnittstellen(value):
    return range(value)

@register.simple_tag
def get_media_prefix():
    from django.conf import settings
    return settings.MEDIA_URL
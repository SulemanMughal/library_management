

# from django.template.Library import filter


# from django.template.Library import filter


from django import template


register = template.Library()

from course.models import *

@register.filter
def statusFind(value):
    if value is True:
        return "Avaiable" 
    return "Not Avaialble"
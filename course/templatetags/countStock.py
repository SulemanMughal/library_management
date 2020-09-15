

# from django.template.Library import filter


# from django.template.Library import filter


from django import template


register = template.Library()

from course.models import *


@register.filter
def countStock(value):
    return bookModel.objects.filter(book = Book.objects.get(id=value), status=True).count()
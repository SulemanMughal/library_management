

# from django.template.Library import filter


# from django.template.Library import filter


from django import template


register = template.Library()


@register.filter
def wordwrapping(value):
    if len(value) >= 80 :
        return value[:31] + " " + value[31:61] + " " + value[61:]
    elif len(value) >= 60:
            return value[:31] + " " + value[31:61] 
    elif len(value) >= 30:
        return value[:31] + " " + value[31:]     
    return value



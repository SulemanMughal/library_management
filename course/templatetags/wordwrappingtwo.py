from django import template


register = template.Library()


@register.filter
def wordwrappingtwo(value):
    if len(value) >= 80 :
        return value[:14] + " " + value[14:28] + " " + value[28: 42] + " " + value[42:56] + " " + value[56: 70] + " " + value[70:]
    elif len(value) >= 60:
            return value[:14] + " " + value[14:28] + " " + value[28: 42] + " " + value[42:56] + " " + value[56:]
    elif len(value) >= 40:
        return value[:14] + " " + value[14:28] + " " + value[28: ]
    elif len(value)>= 20:
        return value[:14] + " " + value[14:] 
    
    return value


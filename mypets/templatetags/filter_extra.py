from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value * arg
    except (Exception,):
        pass
    return ''

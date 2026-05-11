from django import template

register = template.Library()


@register.filter
def split(value, separator=','):
    return [v.strip() for v in str(value).split(separator)]


@register.filter
def trim(value):
    return str(value).strip()


@register.filter
def get_item(lst, index):
    try:
        return lst[int(index)]
    except (IndexError, TypeError):
        return ''

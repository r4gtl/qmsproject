from django import template
from django.template.defaultfilters import floatformat
from django.utils.formats import number_format


'''
Per utilizzare questo custom filter, ricordarsi di inserire a inizio template
{% load custom_filters %}
'''
register = template.Library()





def format_number_dec_thousand(value):
    formatted_value = format(value, ',.2f').replace(',', '|').replace('.', ',').replace('|', '.')
    return formatted_value


register.filter('format_number_dec_thousand', format_number_dec_thousand)

def get_icon_alias(fields, field_name):
    field_data = fields.get(field_name)
    if field_data:
        return field_data['icon_class']
    return None

register.filter('get_icon_alias', get_icon_alias)

def get_alias(fields, field_name):
    field_data = fields.get(field_name)
    if field_data:
        return field_data['alias']
    return None

register.filter('get_alias', get_alias)
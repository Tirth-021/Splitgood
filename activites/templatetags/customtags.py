from django import template
import datetime

register = template.Library()


@register.filter(name='give_date')
def give_date(date_string):
    return date_string.strftime('%d')


@register.filter(name='give_month')
def give_date(date_string):
    return date_string.strftime('%b')

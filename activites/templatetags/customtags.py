from django import template

register = template.Library()


@register.filter(name='give_date')
def give_date(date_string):
    return date_string.strftime('%d')


@register.filter(name='give_month')
def give_date(date_string):
    return date_string.strftime('%b')


@register.filter(name='give_time')
def give_time(date_string):
    return date_string.strftime('%H:%M')


@register.filter(name='check_user')
def check_user(username, request_user):
    return "You" if username == request_user else username

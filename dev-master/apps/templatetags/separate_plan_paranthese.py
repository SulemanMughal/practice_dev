# separate_plan_paranthese


from django import template
from apps.models import *
from django.contrib.auth.models import User

register = template.Library()


def separate_plan_paranthese(value):
    print(value)
    return value
register.filter(separate_plan_paranthese)

from django import template
from apps.models import *
from django.contrib.auth.models import User

from datetime import datetime
from datetime import timedelta
register = template.Library()


def findNextMonth(user_value=None):
    return (datetime.now() + timedelta(days = 30)).strftime("%B")


register.filter(findNextMonth)
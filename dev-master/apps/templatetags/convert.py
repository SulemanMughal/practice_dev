



from django import template
from apps.models import *
from django.contrib.auth.models import User

register = template.Library()

from datetime import datetime

def convert(time):
    # return  datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        return  datetime.utcfromtimestamp(int(time)).strftime('%B %d, %Y')
    except:
        return None

register.filter(convert)
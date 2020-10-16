from django import template
from apps.models import *
from django.contrib.auth.models import User
register = template.Library()

def findUserPhone(user_id):
    try:
        return profileModel.objects.get(user=User.objects.get(id=user_id)).contactNumber
    except:
        return None


register.filter(findUserPhone)
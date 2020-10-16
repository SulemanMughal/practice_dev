

from django import template
from apps.models import *
from django.contrib.auth.models import User

from datetime import datetime
from datetime import timedelta
register = template.Library()


def FindCategoryPlanInfo(user_value=None, value=None):
    try:
        p = plan.objects.get(id = user_value)
        c= category.objects.get(id = p.category.id)
        cp = CategoryPlanName.objects.get(name=p.plan_name)
        if value is not None:
            if int(value) == 1:
                if len(cp.data) == 0:
                    return str("No Data")
                else:
                    return str(cp.data)
            elif int(value) == 2:
                if len(cp.Hotspot) == 0:
                    return str("No Hotspot")
                else:
                    return str(cp.Hotspot)
            elif int(value) == 3:
                if len(cp.streaming) == 0:
                    return str("No Streaming")
                else:
                    return str(cp.streaming)
            elif int(value) == 4:
                if len(cp.international_TD) == 0:
                    return str("No International Texting and Data")
                else:
                    return str(cp.international_TD)
            elif int(value) == 5:
                if len(cp.Talk_Text) == 0:
                    return str("No Talk and Text")
                else:
                    return str(cp.Talk_Text)
        else:
            return p.plan_name
    
    except CategoryPlanName.DoesNotExist:
        if value is not None:
            if int(value) == 1:
                return str("No Data")
            elif int(value) == 2:
                return str("No Hotspot")
            elif int(value) == 3:
                return str("No Streaming")
            elif int(value) == 4:
                return str("No International Texting and Data")
            elif int(value) == 5:
                return str("No Talk and Text")
        else:
            return p.plan_name
    except Exception as e:
        if value is not None:
            if int(value) == 1:
                return str("No Data")
            elif int(value) == 2:
                return str("No Hotspot")
            elif int(value) == 3:
                return str("No Streaming")
            elif int(value) == 4:
                return str("No International Texting and Data")
            elif int(value) == 5:
                return str("No Talk and Text")
        else:
            return p.plan_name


register.filter(FindCategoryPlanInfo)
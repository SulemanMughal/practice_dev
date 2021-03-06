from django import template
from apps.models import plan, category, CategoryPlanName
register = template.Library()
def FindPlanFixedPrice(plan_id=None):
    try:
        p = plan.objects.get(id=plan_id)
        c = category.objects.get(id = p.category.id)
        cp = CategoryPlanName.objects.get(category=c, name=p.plan_name)
        try:
            return int(cp.plan_price)
        except Exception as e:
            return 0
    except Exception as e:
        return 0
register.filter(FindPlanFixedPrice)
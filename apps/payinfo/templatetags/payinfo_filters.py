from django import template
from apps.payinfo.models import Payinfo_order

register = template.Library()

@register.filter
def is_buyer(payinfo,user):
    if user.is_authenticated:
        result = Payinfo_order.objects.filter(payinfo=payinfo,buyer=user,status=2).exists()
        return result
    else:
        return False
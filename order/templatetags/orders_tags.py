
from django.db.models import *
from django.db.models.functions import Concat
from django.template import Library
from order.models import *

register = Library()


@register.simple_tag
def product_count():
    count = Order.objects.annotate(product_count=Concat('items__product_name', Value(' x '), 'items__amount',
                                                        output_field=CharField()))

    return count

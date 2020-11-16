from django.db.models import *
from django.db.models.functions import Concat
from django.views.generic import ListView
from order.models import Order, OrderItem


class OrderListView(ListView):
    model = Order
    template_name = 'order/orders_list.html'

    """def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            fromdate = request.POST['fromdate']
            todate = request.POST['todate']
            return fromdate, todate
        return None"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        que = ExpressionWrapper(F("items__amount") * F('items__product_price'), output_field=DecimalField())

        context['items'] = Order.objects.all().annotate(num=que).annotate(product_count=Concat('items__product_name', Value(' X '), 'items__amount', output_field=CharField()))
        return context


""" def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            fromdate = request.POST['fromdate']
            todate = request.POST['todate']
            try:
                between_date = OrderItem.objects.all().filter(order__create_date__gte=fromdate,
                                                          order__create_date__lte=todate
                                                         )
                between_date_dict = {
                    'between_date': between_date
                }
            except:
                between_date_dict = None
            return render(request, 'order/orders_list.html', between_date_dict)"""


class ResultListView(ListView):
    model = OrderItem
    context_object_name = 'items'
    template_name = 'order/results.html'

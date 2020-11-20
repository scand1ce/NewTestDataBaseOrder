# from django.db import connection, reset_queries
from django.db.models import *
from django.db.models.functions import Concat
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from order.models import Order, OrderItem
from django.contrib.postgres.aggregates.general import StringAgg


class OrderListView(ListView):
    model = Order
    template_name = 'order/orders_list.html'

    def post(self, request, *args, **kwargs):
        if not request.method == "POST":
            data = Order.objects.all().annotate(
                sum_num=ExpressionWrapper(F("items__amount") * F('items__product_price'),
                                          output_field=DecimalField())) \
                .annotate(product_count=Concat('items__product_name', Value(' x '), 'items__amount',
                                               output_field=CharField()
                                               )
                          )
            return render(request, 'order/orders_list.html', {'data': data})
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        between_data = Order.objects.all() \
            .annotate(sum_num=ExpressionWrapper(F("items__amount") * F('items__product_price'),
                                                output_field=DecimalField())) \
            .annotate(product_count=Concat('items__product_name', Value(' x '), 'items__amount',
                                           output_field=CharField()
                                           )
                      ).filter(create_date__gte=fromdate, create_date__lte=todate)

        return render(request, 'order/orders_list.html', {'data': between_data})


class ResultListView(ListView):
    model = Order
    success_url = reverse_lazy('top_results')
    template_name = 'order/top_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders_set_sorted = OrderItem.objects.all() \
            .annotate(name=Concat(Value('Товар - '), 'product_name', output_field=CharField())) \
            .annotate(concat=Concat(Value('Заказ -  '), 'order__number',
                                    Value(',  Цена -  '), 'product_price',
                                    Value(',  Дата -  '), 'order__create_date',
                                    output_field=CharField())) \
            .order_by('-product_name')

        queryset = orders_set_sorted.values('name').order_by('name') \
            .annotate(
            concat_=StringAgg('concat', delimiter='; '),
            customer_name=F('name')
        )

        context['items'] = queryset
        return context




















"""
orders_amount_sum = sum([OrderItem.objects.filter(product_name=item).aggregate(Sum('amount'))['amount__sum']
                                 for item in orders_set_sorted])
#OrderItem.objects.order_by('product_name', 'order__number').distinct('product_name')
        a = OrderItem.objects.select_related("order").all()"""
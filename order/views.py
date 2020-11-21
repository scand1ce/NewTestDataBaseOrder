from django.db import connection, reset_queries
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

        queries = connection.queries
        reset_queries()
        return render(
            request, 'order/orders_list.html', {
                'data': between_data, 'queries': queries, 'fromdate': fromdate, 'todate': todate
            }
        )


class ResultListView(OrderListView):
    success_url = reverse_lazy('top_results')
    template_name = 'order/top_results.html'


    def get_context_data(self, **kwargs):
        fromdate = self.request.GET.get('fromdate')
        todate = self.request.POST.get('todate')
        print(fromdate, '|||||||||', todate)
        orders_set_sorted = OrderItem.objects.all() \
            .annotate(name=Concat(Value('Товар - '), 'product_name', output_field=CharField())) \
            .annotate(concat=Concat(Value('Заказ -  '), 'order__number',
                                    Value(',  Цена -  '), 'product_price',
                                    Value(',  Дата -  '), 'order__create_date',
                                    Value(',  Количество -  '), 'amount',
                                    output_field=CharField())) \
            #.filter(order__create_date__gte=fromdate, order__create_date__lte=todate)

        queryset = orders_set_sorted.values('name').order_by('-name') \
            .annotate(
            concat_=StringAgg('concat', delimiter='; '),
            customer_name=F('name')
        )
        top_amount = queryset.values('name') \
            .annotate(all_amount=ExpressionWrapper(Sum("amount"), output_field=CharField())) \
            .aggregate(Max('all_amount'))['all_amount__max']

        top_product = queryset.values('name') \
            .annotate(sum_num=ExpressionWrapper(F("amount") * F('product_price'), output_field=DecimalField()))

        top_product_max = top_product.order_by('order__id').aggregate(Max('sum_num'))['sum_num__max']

        queries = connection.queries
        reset_queries()
        context = {
            "items": queryset,
            "queries": queries,
            'sum_num__max': top_product_max,
            'all_amount__max': top_amount
        }
        return context

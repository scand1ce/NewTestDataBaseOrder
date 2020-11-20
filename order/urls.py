from django.urls import path
from order.views import *

urlpatterns = [

    path(''.format('orders/'), OrderListView.as_view(), name='orders_list'),
    path('results/', ResultListView.as_view(), name='top_results'),

]
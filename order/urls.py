from django.urls import path
from order.views import OrderListView, ResultListView

urlpatterns = [

    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('results/', ResultListView.as_view(), name='results'),

]
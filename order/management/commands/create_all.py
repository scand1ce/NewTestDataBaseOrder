import datetime
import random
from decimal import Decimal

from django.core.management import BaseCommand
from order.models import Order, OrderItem


class Command(BaseCommand):
    help = u'Создание случайных заказов в БД'

    def add_arguments(self, parser):
        parser.add_argument('orders', type=int, help=u'Количество создаваемых заказов')

    def handle(self, *args, **kwargs):
        orders = kwargs['orders']
        first_date = datetime.datetime(day=1, month=1, year=2018, hour=9, minute=0)
        end = datetime.datetime.now()

        for num in range(1, orders + 1):
            Order.objects.create(
                number=num,
                create_date=first_date + datetime.timedelta(
                    seconds=random.randint(
                        0, int(
                            (end - first_date).total_seconds()
                        )
                    )
                )
            )

        for item in Order.objects.all():
            OrderItem.objects.create(
                order=Order.objects.get(pk=item.pk),
                product_name=random.randint(1, 100),
                product_price=random.randint(100, 9999),
                amount=random.randint(1, 10)
            )
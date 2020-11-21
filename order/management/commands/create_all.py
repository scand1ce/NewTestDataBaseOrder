import datetime
import random
from django.core.management import BaseCommand
from order.models import Order, OrderItem


class Command(BaseCommand):
    help = u'Создание случайных заказов с товарами в БД'

    def add_arguments(self, parser):
        parser.add_argument('orders', type=int, help=u'Количество создаваемых заказов (товары для заказов'
                                                     u' создаются в случайном '
                                                     u'количестве в диапазоне 1-10). '
                                                     u'Принимается позиционный аргумент любое положительное '
                                                     u'целочисленное значение.')

    def handle(self, *args, **kwargs):
        orders = kwargs['orders']
        first_date = datetime.datetime(year=2017, month=12, day=31,  hour=8, minute=0)

        for num in range(1, orders + 1):
            Order.objects.create(
                number=num,
                create_date=first_date + datetime.timedelta(days=num, hours=num)
            )

        for item in Order.objects.all():
            OrderItem.objects.create(
                order=Order.objects.get(pk=item.pk),
                product_name=random.randint(1, 100),
                product_price=random.randint(100, 9999),
                amount=random.randint(1, 10)
            )

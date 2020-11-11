from django.db import models


"""Схема БД:
    Заказ - 
    
    Order (
    number - IntegerField, 
    created_date - DateTimeField
    )
    
    
    Элемент заказа - 
    
    OrderItem (
    order - ForeignKey, 
    product_name - CharField, 
    product_price - DecimalField, 
    amount - IntegerField
    )
    """


class Order(models.Model):
    number = models.IntegerField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=20,  decimal_places=0, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.product_name
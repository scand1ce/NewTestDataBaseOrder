from django.db import models


class Order(models.Model):
    number = models.IntegerField()
    create_date = models.DateTimeField()

    def __str__(self):
        return str(self.number)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.product_name)

    class Meta:
        ordering = ['-order']

from django.db import models
from django.core.exceptions import ValidationError

class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'orders_app'

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than 0')

    def __str__(self):
        return f"Order {self.id} (User: {self.user_id}, Product: {self.product_id})"


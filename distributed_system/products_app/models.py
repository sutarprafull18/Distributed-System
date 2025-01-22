from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'products_app'

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required')
        if self.price <= 0:
            raise ValidationError('Price must be greater than 0')

    def __str__(self):
        return f"{self.name} (${self.price})"


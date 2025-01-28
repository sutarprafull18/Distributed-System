from django.db import models
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        app_label = 'users'

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValidationError('Invalid email format')

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'products'

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required')
        if self.price <= 0:
            raise ValidationError('Price must be greater than 0')

class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'orders'

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than 0')


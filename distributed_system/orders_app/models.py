from django.db import models
from users_app.models import User
from products_app.models import Product


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'orders_app'
        db_table = 'orders_app_order'

    def save(self, *args, **kwargs):
        # Skip saving if quantity is not positive
        if self.quantity <= 0:
            return None

        # Check if user_id exists in users_db
        user_exists = User.objects.using('users_db').filter(id=self.user_id).exists()
        if not user_exists:
            return None

        # Check if product_id exists in products_db
        product_exists = Product.objects.using('products_db').filter(id=self.product_id).exists()
        if not product_exists:
            return None

        super().save(using='orders_db')
        return self

    def __str__(self):
        return f"Order {self.id} - User: {self.user_id}, Product: {self.product_id}"
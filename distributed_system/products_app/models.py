from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True,blank=False,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'products_app'
        db_table = 'products_app_product'

    def save(self, *args, **kwargs):
        # Skip saving if price is negative
        if self.price < 0:
            return None

        # Check for existing product name
        existing_product = Product.objects.using('products_db').filter(name=self.name).first()
        if existing_product:
            if existing_product.id != self.id:
                return None
            else:
                # Update existing product
                existing_product.price = self.price
                super(Product, existing_product).save(using='products_db')
                return existing_product

        super().save(using='products_db')
        return self

    def __str__(self):
        return f"{self.id} - {self.name} (${self.price})"
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    image    = models.ImageField(
                   upload_to='product_images/',
                   blank=True,            # allow products without an image
                   null=True
               )

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered  = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity}×{self.product.name}"

class Order(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    items          = models.ManyToManyField(OrderItem)
    name           = models.CharField(max_length=100)
    phone          = models.CharField(max_length=20)
    address        = models.TextField()
    payment_method = models.CharField(max_length=50, default='Cash On Delivery')
    amount_to_pay  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ordered_date   = models.DateTimeField(auto_now_add=True)
    ordered        = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.username}"

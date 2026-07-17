from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_products')
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class BuyOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    price = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.buyer} - {self.product} - {self.price}원'
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Notification(models.Model):
    TYPE_CHOICES = [
        ('trade', '거래 성사'),
        ('stock', '입고 알림'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='trade')
    email_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.message}'
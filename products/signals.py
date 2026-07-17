from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Product
from notifications.models import Notification

@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):
    if created:
        product = instance
        users = User.objects.exclude(id=product.seller.id)

        for user in users:
            Notification.objects.create(
                user=user,
                product=product,
                message=f"'{product.title}' 상품이 등록되었어요.",
                notification_type='stock',
                email_sent=False
            )
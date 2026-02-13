from django.db.models.signals import post_save
from django.dispatch import receiver

from day_8.models import Payment, PaymentLog


@receiver(post_save, sender=Payment)
def payment_save_handler(sender, instance, created, **kwargs):
    if created:
        PaymentLog.objects.create(payment=instance, message="Payment created")
    else:
        PaymentLog.objects.create(payment=instance, message="Payment updated")

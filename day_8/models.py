from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus,
        default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class ProviderType(models.TextChoices):
    UNSPECIFIED = "unspecified", "Unspecified"
    STRIPE = "stripe", "Stripe"
    FAKE_PROVIDER = "fake provider", "Fake Provider"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus,
        default=PaymentStatus.PENDING
    )
    provider = models.CharField(
        max_length=20,
        choices=ProviderType,
        default=ProviderType.UNSPECIFIED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order"],
                condition=Q(status=PaymentStatus.SUCCESS),
                name="unique_success_payment_per_order"
            )
        ]


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="logs")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

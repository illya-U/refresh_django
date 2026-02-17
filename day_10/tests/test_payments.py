from django.test import TestCase

from django.contrib.auth.models import User

from day_10.models import Order, OrderStatus, Payment, PaymentStatus


class PaymentTest(TestCase):
    def test_create_payment(self):
        user = User.objects.create(username="testuser", password="testpassword", email="111@gmail.com")
        order = Order.objects.create(user=user, amount=10, status=OrderStatus.PENDING)
        payment = Payment.objects.create(order=order, amount=10, status=PaymentStatus.PENDING)

        payment.save()

        payment.refresh_from_db()
        assert payment == Payment.objects.get(id=payment.id)
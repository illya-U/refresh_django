from django.db import transaction
from rest_framework.exceptions import ValidationError

from day_8.models import OrderStatus, Order


class OrderService:
    def cancel_order(self, order_id):
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=order_id)
            self._cancel_business_validation(order)
            self._cancel_payment(order)
        return order

    def _cancel_business_validation(self, order):
        if order.status != OrderStatus.PENDING:
            raise ValidationError("Only pending orders can be cancelled.")

        return order

    def _cancel_payment(self, order):
        order.status = OrderStatus.CANCELLED
        order.save()

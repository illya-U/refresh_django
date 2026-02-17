from django.contrib.auth.models import User
from rest_framework import serializers

from day_10.models import Order, OrderStatus, Payment, ProviderType, PaymentStatus, PaymentLog
from day_10.services.OrderService import OrderService
from day_10.services.PaymentService import PaymentService


class DefaultOrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "username",
            "amount",
            "status",
        ]


class CreateOrderSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Order.objects.create(
            user=validated_data['user'],
            amount=validated_data['amount'],
            status=OrderStatus.PENDING,
        )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class CancelOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(write_only=True)

    username = serializers.CharField(source='user.username', read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        order = OrderService().cancel_order(validated_data['order_id'])
        return order

    def validate_order_id(self, value):
        try:
            Order.objects.get(id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order does not exist.")
        return value


class DefaultPaymentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='order.user.username', read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            'order',
            'amount',
            'status',
            'provider',
            'username',
            'created_at',
        ]


class CreatePaymentSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all()
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    provider = serializers.ChoiceField(choices=ProviderType)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        order = data['order']
        if order.status in [OrderStatus.PAID, OrderStatus.CANCELLED]:
            raise serializers.ValidationError("Failed payments cannot be created.")
        if order.amount != data['amount']:
            raise serializers.ValidationError("Payment amount must match order amount.")
        return data

    def create(self, validated_data):
        return Payment.objects.create(
            order=validated_data['order'],
            status=PaymentStatus.PENDING,
            amount=validated_data['amount'],
            provider=validated_data['provider'],
        )


class CancelPaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField(write_only=True)

    username = serializers.CharField(source='order.user.username', read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    provider = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        order = PaymentService().cancel_payment(validated_data['payment_id'])
        return order

    def validate_payment_id(self, value):
        try:
            Payment.objects.get(id=value)
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Order does not exist.")
        return value


class PayPaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField(write_only=True)

    username = serializers.CharField(source='order.user.username', read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    provider = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        payment = PaymentService().pay_order(validated_data['payment_id'])
        return payment

    def validate_payment_id(self, value):
        try:
            Payment.objects.get(id=value)
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Payment does not exist.")
        return value


class DefaultPaymentLogsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='payment.order.user.username', read_only=True)
    payment = DefaultPaymentSerializer(read_only=True)
    order = DefaultOrderSerializer(source='payment.order', read_only=True)

    class Meta:
        model = PaymentLog
        fields = [
            "id",
            "username",
            "payment",
            "order",
            "message",
            "created_at",
        ]

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from unittest.mock import patch
from django.test import TestCase

from day_10.models import Order, Payment, PaymentStatus, ProviderType
from day_10.views import OrdersApiView

class OrdersApiViewTest(TestCase):
    @patch("day_10.views.Order")
    @patch("day_10.views.DefaultOrderSerializer")
    def test_get(self, DefaultOrderSerializer_mock, Order_mock):

        factory = APIRequestFactory()
        request = factory.get("/orders/")
        OrdersApiView.as_view()(request)

        Order_mock.objects.select_related.assert_called_once_with("user")
        DefaultOrderSerializer_mock.assert_called_once_with(Order_mock.objects.select_related.return_value, many=True)


class PaymentsApiView(APITestCase):
    def test_get(self):
        user = User.objects.create(username="test", password="1111", email="")
        order = Order.objects.create(user=user, amount=100.00)
        payment = Payment.objects.create(order=order, amount=100.00)

        url = f"/day_10/payments/{order.pk}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data[0]["order"] == order.id
        assert response.data[0]["amount"] == "100.00"
        assert response.data[0]["status"] == "pending"
        assert response.data[0]["provider"] == "unspecified"
        assert response.data[0]["username"] == payment.order.user.username









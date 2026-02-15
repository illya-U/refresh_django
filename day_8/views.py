from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from day_8.models import Order, Payment, PaymentLog
from day_8.serializers import DefaultOrderSerializer, CreateOrderSerializer, CancelOrderSerializer, \
    DefaultPaymentSerializer, CreatePaymentSerializer, CancelPaymentSerializer, PayPaymentSerializer, \
    DefaultPaymentLogsSerializer


# Create your views here.
class OrdersApiView(APIView):
    def get(self, request):
        orders = Order.objects.select_related("user")
        serializer = DefaultOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class OrdersRetrieveApiView(RetrieveAPIView):
    queryset = Order.objects.select_related("user")
    serializer_class = DefaultOrderSerializer


class CancelOrderApiView(APIView):
    def post(self, request, pk):
        serializer = CancelOrderSerializer(data={"order_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

#-----------------------------------------------------------------------------#


class PaymentsApiView(APIView):
    def get(self, request):
        orders = Payment.objects.select_related("order__user")
        serializer = DefaultPaymentSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class PaymentRetrieveApiView(APIView):
    def get(self, request, fk):
        payments = Payment.objects.select_related("order__user").filter(order_id__exact=fk)
        serializer = DefaultPaymentSerializer(payments, many=True)
        return Response(serializer.data)


class PayPaymentApiView(APIView):
    def post(self, request, pk=None):
        serializer = PayPaymentSerializer(data={"payment_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class CancelPaymentApiView(APIView):
    def post(self, request, pk=None):
        serializer = CancelPaymentSerializer(data={"payment_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class PaymentLogsListApiView(ListAPIView):
    queryset = PaymentLog.objects.select_related("payment__order__user")
    serializer_class = DefaultPaymentLogsSerializer

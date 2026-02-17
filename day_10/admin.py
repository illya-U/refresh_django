from django.contrib import admin

from day_10.models import Order, Payment, PaymentLog

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(PaymentLog)

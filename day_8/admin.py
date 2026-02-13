from django.contrib import admin

from day_8.models import Order, Payment, PaymentLog

# Register your models here.

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(PaymentLog)
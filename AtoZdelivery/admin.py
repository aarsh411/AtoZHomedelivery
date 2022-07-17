from django.contrib import admin
from .models import Customer,tasker,orders
# Register your models here.
admin.site.register(Customer)
admin.site.register(tasker)
admin.site.register(orders)

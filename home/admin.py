from django.contrib import admin
from .models import Check, MarketItems, Cart
# Register your models here.

admin.site.register(Check)
admin.site.register(MarketItems)
admin.site.register(Cart)
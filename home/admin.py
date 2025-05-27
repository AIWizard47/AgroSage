from django.contrib import admin
from .models import Check, MarketItems, Cart, Feedback, Category
# Register your models here.

admin.site.register(Category)
admin.site.register(Check)
admin.site.register(MarketItems)
admin.site.register(Cart)
admin.site.register(Feedback)
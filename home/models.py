from django.db import models
from django.contrib.auth.models import User  # Correct import

# Create your models here.
class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_farmer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

class MarketItems(models.Model):
    items_name = models.CharField(max_length=1000)
    items_description = models.TextField(max_length=1000)
    item_price = models.IntegerField()
    item_image = models.ImageField(upload_to='market_items/')
    items_weight = models.IntegerField()
    def __str__(self):
        return self.items_name
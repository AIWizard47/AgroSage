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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.OneToOneField(MarketItems, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class Feedback(models.Model):
    email = models.EmailField()
    description = models.TextField(max_length=10000)
    
    def __str__(self):
        return self.email
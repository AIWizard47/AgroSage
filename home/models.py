from django.db import models
from django.contrib.auth.models import User  # Correct import

# Create your models here.
class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(max_length=10,default=7759059001)
    is_farmer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name 

class MarketItems(models.Model):
    farmer = models.ForeignKey(User,on_delete=models.CASCADE)
    items_name = models.CharField(max_length=1000)
    items_description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)   # e.g. “Fertilizer”, “Tool”
    item_price = models.IntegerField()
    item_image = models.ImageField(upload_to='market_items/')
    items_weight = models.IntegerField()
    min_weight = models.IntegerField(default=0)
    item_rating = models.IntegerField(default=0)    
    location = models.CharField(max_length=300,default="Neelbad, Bhopal, Mp")
    
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
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} ({self.email})'
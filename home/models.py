from django.db import models
from django.contrib.auth.models import User  # Correct import

# Create your models here.
class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_farmer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

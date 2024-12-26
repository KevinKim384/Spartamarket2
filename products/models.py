from django.db import models
from django.conf import settings
from accounts.models import Users

# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='products') 

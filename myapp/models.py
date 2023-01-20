from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# This is a product model
class Products(models.Model): # It's better to define class name not plural
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):  # Canonical URL
        return reverse('myapp:products')
    
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=300)
    image = models.ImageField(blank=True, upload_to='images')

class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(to='Products', on_delete=models.PROTECT)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

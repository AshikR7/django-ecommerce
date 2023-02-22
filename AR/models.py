from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class registermodel(models.Model):
    name = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    shop_id = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=20)


class product_upload_model(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    imgfile=models.ImageField(upload_to='AR/static/products')

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    imgfile = models.ImageField()

class wishlist(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    imgfile = models.ImageField()

class buy(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    quantity=models.IntegerField()

class customercard(models.Model):
    cardname=models.CharField(max_length=30)
    cardnumber=models.CharField(max_length=30)
    cardexpiry=models.CharField(max_length=30)
    code=models.CharField(max_length=30)

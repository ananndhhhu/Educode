
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='course/')
    modules = models.IntegerField(null=True,)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

class Payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="payments",null=True,blank=True)
    learning_mode = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    payment_status = models.CharField(max_length=20,default="Pending")
    amount = models.IntegerField(default=1000)

    created = models.DateTimeField(auto_now_add=True)
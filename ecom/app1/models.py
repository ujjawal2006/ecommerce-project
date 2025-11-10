from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
     STATE_CHOICES = [
        ('UP', 'Uttar Pradesh'),
        ('MH', 'Maharashtra'),
        ('DL', 'Delhi'),
        ('RJ', 'Rajasthan'),
        ('BH', 'Bihar')
    ]
     user = models.OneToOneField(User, on_delete=models.CASCADE) 
     fname=models.CharField(max_length=45)
     lname=models.CharField(max_length=33)
     email=models.EmailField()
     pnumber=models.IntegerField(max_length=12)
     address=models.CharField(max_length=245)
     city=models.CharField(max_length=233)
     state=models.CharField(max_length=2, choices=STATE_CHOICES)
     zip=models.IntegerField(max_length=7)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FullName=models.CharField(max_length=100)
    MobileNumber=models.IntegerField(max_length=12)
    Pincode=models.IntegerField(max_length=6)
    Loclity=models.CharField(max_length=40)
    Add=models.CharField(max_length=100)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=40)
    landamrk=models.CharField(max_length=30)
    APhone=models.CharField(max_length=12)

    


  


from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)  # 👈 New field


    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"
    
from django.contrib.auth.models import User

class Bid(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} on {self.car}"



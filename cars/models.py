from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Car Categories'

class Car(models.Model):
    TRANSMISSION_CHOICES = (
        ('A', 'Automatic'),
        ('M', 'Manual'),
    )
    
    FUEL_CHOICES = (
        ('P', 'Petrol'),
        ('D', 'Diesel'),
        ('E', 'Electric'),
        ('H', 'Hybrid'),
    )
    
    CONDITION_CHOICES = (
        ('N', 'New'),
        ('U', 'Used'),
    )
    
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    mileage = models.IntegerField()
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES)
    engine_size = models.CharField(max_length=50)
    power = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    features = models.TextField()
    main_photo = models.ImageField(upload_to='cars/')
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.year} {self.brand} {self.title}"
    
    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'pk': self.pk})

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    
    def __str__(self):
        return f"Image for {self.car}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
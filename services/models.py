from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ServiceProvider(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]
    
    # Basic Info
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=15)
    profession = models.CharField(max_length=50)
    bio = models.TextField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    
    # Location
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    address = models.TextField(blank=True, default='')
    
    # Service Info
    service_type = models.CharField(max_length=50, default='General')
    experience_years = models.IntegerField(default=0)
    
    # Pricing
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    call_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Status & Rating
    rating = models.FloatField(default=0.0)
    verified = models.BooleanField(default=False)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    total_jobs = models.IntegerField(default=0)
    
    # Metadata
    member_since = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ['-rating', '-total_jobs']
    
    def __str__(self):
        return f"{self.name} - {self.profession}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Relationships
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
    # Customer Info
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(blank=True, default='')
    customer_address = models.TextField()
    
    # Booking Details
    service = models.CharField(max_length=100)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    notes = models.TextField(blank=True, default='')
    
    # Status & Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"Booking: {self.customer_name} - {self.service} ({self.status})"
from django.db import models
from django.utils import timezone

class ServiceProvider(models.Model):
    # Basic Info
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
    availability = models.CharField(max_length=50, default='Available')
    total_jobs = models.IntegerField(default=0)
    
    # Metadata
    member_since = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ['-rating', '-total_jobs']
    
    def __str__(self):
        return f"{self.name} - {self.profession}"
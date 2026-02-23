from django.db import models

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
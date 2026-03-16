from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, default = None)

    def __str__(self):
        return f"Profile: {self.user.username}"
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    
    def __str__(self):
        return f"Address: {self.city}, {self.postal_code}, {self.country}"
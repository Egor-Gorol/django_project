from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Address


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        address = Address.objects.create(user=instance, street='', city='')
        Profile.objects.create(user=instance, address=address)
 
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
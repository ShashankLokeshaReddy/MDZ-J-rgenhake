from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CustomerProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = CustomerProfile()
        profile.user = instance
        profile.benutzername = instance.username

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.customerprofile.save()
    except:
        print('Error occurred while saving customer profile for user')
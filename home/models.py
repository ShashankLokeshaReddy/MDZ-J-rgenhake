from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from colorfield.fields import ColorField
import os

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ust_id = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    unternehmensname = models.CharField(max_length=255, null=True)
    land = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    telefonnummer = models.CharField(max_length=20, null=True)
    ansprechpartner = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username  # or any other field to represent the object as a string
    
    def save(self):
        super().save()

        img = PILImage.open(self.image.path)

        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Akkuvariante(models.Model):
    akkuvariante_name = models.CharField(max_length=255, primary_key=True)
    akkuvariante_image_path = models.ImageField(default='default.png', upload_to='Akkuvariante')
    akkuvariante_price = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        # Ensure the uploaded image has the filename 'akkuvariante_name.png'
        if self.akkuvariante_image_path:
            filename = f"{self.akkuvariante_name}.png"
            self.akkuvariante_image_path.name = os.path.join(filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.akkuvariante_name  # or any other field to represent the object as a string

class Kabelvariante(models.Model):
    kabelvariante_name = models.CharField(max_length=255, primary_key=True)
    kabelvariante_image_path = models.ImageField(default='default.png', upload_to='Kabelvariante')
    # Maße
    main_part_min_length = models.IntegerField(null=True)
    main_part_max_length = models.IntegerField(null=True)
    split_part_min_length = models.IntegerField(null=True)
    split_part_max_length = models.IntegerField(null=True)
    masse_image_path =models.ImageField(default='default.png', upload_to='Maße')
    # Splits in the cabel
    splits = models.IntegerField(null=True) # No. of splits x2 is 1 for straight and 2 for Y
    kabel_price_per_meter = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.kabelvariante_image_path:
            filename = f"{self.kabelvariante_name}.png"
            self.kabelvariante_image_path.name = os.path.join(filename)

        if self.masse_image_path:
            filename = f"{self.kabelvariante_name}Maße.png"
            self.masse_image_path.name = os.path.join(filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.kabelvariante_name  # or any other field to represent the object as a string

class Schnittstelle(models.Model):
    schnittstelle_name = models.CharField(max_length=255, primary_key=True)
    schnittstelle_image_path = models.ImageField(default='default.png', upload_to='Schnittstellen')
    schnittstelle_price = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.schnittstelle_image_path:
            filename = f"{self.schnittstelle_name}.png"
            self.schnittstelle_image_path.name = os.path.join(filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.schnittstelle_name  # or any other field to represent the object as a string

class Color(models.Model):
    color_name = models.CharField(max_length=255, primary_key=True)
    color_value = ColorField(format="hex") # hex or hexa (https://pypi.org/project/django-colorfield/)

    def __str__(self):
        return self.color_name  # or any other field to represent the object as a string

class UILabel(models.Model):
    label_key = models.CharField(max_length=255, primary_key=True)
    label_value = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.label_key  # or any other field to represent the object as a string

class Image(models.Model):
    image_path = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.image_path  # or any other field to represent the object as a string

class Order(models.Model):
    order_number = models.CharField(max_length=255, primary_key=True)
    ust_id = models.CharField(max_length=50, null=True)
    order_date = models.DateTimeField(null=True)
    order_details = models.CharField(max_length=255,null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.image_path  # or any other field to represent the object as a string

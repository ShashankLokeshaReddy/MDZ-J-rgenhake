from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from colorfield.fields import ColorField
import os
import uuid

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

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Akkuvariante.objects.filter(akkuvariante_name=self.akkuvariante_name).first()

        # If there's an existing object, delete its image before saving the new one
        if existing_object and existing_object.akkuvariante_image_path:
            existing_image_path = existing_object.akkuvariante_image_path.path
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

        # Ensure the uploaded image has the filename 'akkuvariante_name.png'
        if self.akkuvariante_image_path:
            filename = f"{self.akkuvariante_name}.png"
            self.akkuvariante_image_path.name = os.path.join('Akkuvariante', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.akkuvariante_name

class Kabelvariante(models.Model):
    kabelvariante_name = models.CharField(max_length=255, primary_key=True)
    kabelvariante_image_path = models.ImageField(default='default.png', upload_to='Kabelvariante')
    main_part_min_length = models.IntegerField(null=True)
    split_part_min_length = models.IntegerField(null=True)
    masse_image_path = models.ImageField(default='default.png', upload_to='Maße')
    splits = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Kabelvariante.objects.filter(kabelvariante_name=self.kabelvariante_name).first()

        # If there's an existing object, delete its images before saving the new ones
        if existing_object:
            if existing_object.kabelvariante_image_path:
                existing_image_path = existing_object.kabelvariante_image_path.path
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)

            if existing_object.masse_image_path:
                existing_masse_image_path = existing_object.masse_image_path.path
                if os.path.exists(existing_masse_image_path):
                    os.remove(existing_masse_image_path)

        # Ensure the uploaded images have the correct filenames
        if self.kabelvariante_image_path:
            filename = f"{self.kabelvariante_name}.png"
            self.kabelvariante_image_path.name = os.path.join('Kabelvariante', filename)

        if self.masse_image_path:
            filename = f"{self.kabelvariante_name}Maße.png"
            self.masse_image_path.name = os.path.join('Maße', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.kabelvariante_name

class Schnittstelle(models.Model):
    schnittstelle_name = models.CharField(max_length=255, primary_key=True)
    schnittstelle_image_path = models.ImageField(default='default.png', upload_to='Schnittstellen')

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Schnittstelle.objects.filter(schnittstelle_name=self.schnittstelle_name).first()

        # If there's an existing object, delete its image before saving the new one
        if existing_object and existing_object.schnittstelle_image_path:
            existing_image_path = existing_object.schnittstelle_image_path.path
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

        # Ensure the uploaded image has the filename 'schnittstelle_name.png'
        if self.schnittstelle_image_path:
            filename = f"{self.schnittstelle_name}.png"
            self.schnittstelle_image_path.name = os.path.join('Schnittstellen', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.schnittstelle_name

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

class InCartItem(models.Model):
    item_number = models.CharField(max_length=255, primary_key=True)
    ust_id = models.CharField(max_length=50, null=True)
    # item_details = models.CharField(max_length=255, null=True)
    akkuvariante = models.CharField(max_length=255, null=True)
    kabelvariante = models.CharField(max_length=255, null=True)
    schnittstelle = models.CharField(max_length=255, null=True)
    masse = models.CharField(max_length=255, null=True)
    quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)
    total = models.FloatField(null=True)

    def __str__(self):
        return self.item_number

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Ordered', 'Ordered'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ust_id = models.CharField(max_length=50, null=True)
    order_date = models.DateTimeField(null=True)
    order_details = models.CharField(max_length=255, null=True)
    order_status = models.CharField(max_length=255, null=True, choices=ORDER_STATUS_CHOICES, default='Ordered')

    def update_status(self, new_status):
        """
        Update the order status and save the instance.
        """
        self.order_status = new_status
        self.save()

    def place_order(self):
        """
        Set the order status to 'Ordered'.
        """
        self.update_status('Ordered')

    def deliver_order(self):
        """
        Set the order status to 'Delivered'.
        """
        self.update_status('Delivered')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=False)
    item_number = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ust_id = models.CharField(max_length=50, null=True)
    # item_details = models.CharField(max_length=255, null=True)
    akkuvariante = models.CharField(max_length=255, null=True)
    kabelvariante = models.CharField(max_length=255, null=True)
    schnittstelle = models.CharField(max_length=255, null=True)
    masse = models.CharField(max_length=255, null=True)
    quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)
    total = models.FloatField(null=True)

class PreisListe(models.Model):
    kabelvariante = models.CharField(max_length=50, null=True)
    gehause = models.CharField(max_length=50, null=True)
    leitung = models.CharField(max_length=50, null=True)
    lange = models.CharField(max_length=50, null=True)
    qty_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_25 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_100 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_250 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_500 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_1000 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_2000 = models.DecimalField(max_digits=10, decimal_places=2, null=True)

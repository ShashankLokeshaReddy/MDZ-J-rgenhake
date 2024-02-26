from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from colorfield.fields import ColorField
import os
import uuid
from django.utils.deconstruct import deconstructible
from home.storage import OverwriteStorage
from django.utils.text import slugify

def get_img_upload_path_profile(instance, filename):
    return f"profile_pics/{instance.benutzername}.{filename.split('.')[-1]}"

def get_img_upload_path_akku(instance, filename):
    return f"Akkuvariante/{convert_to_url_format(instance.akkuvariante_name)}.{filename.split('.')[-1]}"

def get_img_upload_path_kabel(instance, filename):
    return f"Kabelvariante/{convert_to_url_format(instance.kabelvariante_name)}.{filename.split('.')[-1]}"

def get_img_upload_path_masse(instance, filename):
    return f"Maße/{convert_to_url_format(instance.kabelvariante_name)}.{filename.split('.')[-1]}"

def get_img_upload_path_schnittstelle(instance, filename):
    return f"Schnittstellen/{convert_to_url_format(instance.schnittstelle_name)}.{filename.split('.')[-1]}"

def convert_to_url_format(input_string):
    # Replace spaces with underscores and hyphens with double underscores
    formatted_string = input_string.replace(' ', '_').replace('–', '').replace('-', '__')
    return formatted_string

def get_img_upload_path_general_images(instance, filename):
    return f"General/{convert_to_url_format(instance.general_image_name)}.{filename.split('.')[-1]}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    benutzername = models.CharField(max_length=50, primary_key=True)
    ust_id = models.CharField(max_length=20, null=True)
    image = models.ImageField(default='General/default.png', upload_to=get_img_upload_path_profile, storage=OverwriteStorage())
    unternehmensname = models.CharField(max_length=255, null=True)
    land = models.CharField(max_length=100, null=True)
    adresse = models.TextField(null=True)
    plz = models.CharField(max_length=5, null=True)
    telefonnummer = models.CharField(max_length=20, null=True)
    ansprechpartner = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Kundenprofil'
        verbose_name_plural = 'Kundenprofile'

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
    akkuvariante_image_path = models.ImageField(default='default.png', upload_to=get_img_upload_path_akku, storage=OverwriteStorage())

    class Meta:
        verbose_name = 'Akkuvariante'
        verbose_name_plural = 'Akkuvarianten'

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Akkuvariante.objects.filter(akkuvariante_name=self.akkuvariante_name).first()

        # If there's an existing object and a new file is uploaded, delete its old image before saving the new one
        if existing_object and self.akkuvariante_image_path != existing_object.akkuvariante_image_path:
            existing_image_path = existing_object.akkuvariante_image_path.path
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

        # Ensure the uploaded image has the filename 'akkuvariante_name.png'
        if self.akkuvariante_image_path:
            filename = f"{convert_to_url_format(self.akkuvariante_name)}.png"
            self.akkuvariante_image_path.name = os.path.join('Akkuvariante', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.akkuvariante_name

class Kabelvariante(models.Model):
    kabelvariante_name = models.CharField(max_length=255, primary_key=True, verbose_name="Kabelvariante")
    kabelvariante_image_path = models.ImageField(default='default.png', upload_to=get_img_upload_path_kabel, storage=OverwriteStorage(), verbose_name="Abbildungspfad")
    main_part_min_length = models.IntegerField(null=True, verbose_name="Mindestlänge der Hauptleitung")
    split_part_min_length = models.IntegerField(null=True, verbose_name="Mindestlänge der Zweigleitungen")
    masse_image_path = models.ImageField(default='default.png', upload_to=get_img_upload_path_masse, storage=OverwriteStorage(), verbose_name="Abbildungspfad für beschriftete Abbildung")
    splits = models.IntegerField(null=True, verbose_name="Splits")

    class Meta:
        verbose_name = "Kabelvariante"
        verbose_name_plural = "Kabelvarianten"

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Kabelvariante.objects.filter(kabelvariante_name=self.kabelvariante_name).first()

        # If there's an existing object, delete its images before saving the new ones
        if existing_object:
            if existing_object.kabelvariante_image_path and self.kabelvariante_image_path != existing_object.kabelvariante_image_path:
                existing_image_path = existing_object.kabelvariante_image_path.path
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)

            if existing_object.masse_image_path and self.masse_image_path != existing_object.masse_image_path:
                existing_masse_image_path = existing_object.masse_image_path.path
                if os.path.exists(existing_masse_image_path):
                    os.remove(existing_masse_image_path)

        # Ensure the uploaded images have the correct filenames
        if self.kabelvariante_image_path:
            filename = f"{convert_to_url_format(self.kabelvariante_name)}.png"
            self.kabelvariante_image_path.name = os.path.join('Kabelvariante', filename)

        if self.masse_image_path:
            filename = f"{convert_to_url_format(self.kabelvariante_name)}Maße.png"
            self.masse_image_path.name = os.path.join('Maße', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.kabelvariante_name

class Schnittstelle(models.Model):
    schnittstelle_name = models.CharField(max_length=255, primary_key=True, verbose_name="Bezeichnung")
    schnittstelle_image_path = models.ImageField(default='default.png', upload_to=get_img_upload_path_schnittstelle, storage=OverwriteStorage(), verbose_name="Abbildungspfad")

    class Meta:
        verbose_name = "Schnittstelle"
        verbose_name_plural = "Schnittstellen"

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Schnittstelle.objects.filter(schnittstelle_name=self.schnittstelle_name).first()

        # If there's an existing object, delete its image before saving the new one
        if existing_object and existing_object.schnittstelle_image_path and self.schnittstelle_image_path != existing_object.schnittstelle_image_path:
            existing_image_path = existing_object.schnittstelle_image_path.path
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

        # Ensure the uploaded image has the filename 'schnittstelle_name.png'
        if self.schnittstelle_image_path:
            filename = f"{convert_to_url_format(self.schnittstelle_name)}.png"
            self.schnittstelle_image_path.name = os.path.join('Schnittstellen', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.schnittstelle_name

class Color(models.Model):
    color_name = models.CharField(max_length=255, primary_key=True, verbose_name="Kategorie")
    color_value = ColorField(format="hex", verbose_name="Farbcode") # hex or hexa (https://pypi.org/project/django-colorfield/)

    class Meta:
        verbose_name = 'Farbe'
        verbose_name_plural = 'Farben'

    def __str__(self):
        return self.color_name  # or any other field to represent the object as a string

class UILabel(models.Model):
    label_key = models.CharField(max_length=255, primary_key=True, verbose_name="Label")
    label_value = models.CharField(max_length=1000,null=True, verbose_name="Labelwert")

    class Meta:
        verbose_name = "UI-Label"
        verbose_name_plural = "UI-Labels"

    def __str__(self):
        return self.label_key  # or any other field to represent the object as a string

class Image(models.Model):
    general_image_name = models.CharField(max_length=255, primary_key=True, verbose_name="Bezeichnung")
    general_image_path = models.ImageField(default='default.png', upload_to=get_img_upload_path_general_images, storage=OverwriteStorage(), verbose_name="Abbildungspfad")

    class Meta:
        verbose_name = 'Abbildung'
        verbose_name_plural = 'Abbildungen'

    def save(self, *args, **kwargs):
        # Check if there's an existing object with the same name
        existing_object = Image.objects.filter(general_image_name=self.general_image_name).first()

        # If there's an existing object and a new file is uploaded, delete its old image before saving the new one
        if existing_object and self.general_image_path != existing_object.general_image_path:
            existing_image_path = existing_object.general_image_path.path
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)

        # Ensure the uploaded image has the filename 'general_image_name.png'
        if self.general_image_path:
            filename = f"{convert_to_url_format(self.general_image_name)}.png"
            self.general_image_path.name = os.path.join('General', filename)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.general_image_name

class InCartItem(models.Model):
    CAN_BUS_STATUS_CHOICES = [
        ('Ja', 'Ja'),
        ('Nein', 'Nein'),
    ]
    item_nummer = models.CharField(max_length=255, primary_key=True, verbose_name="Artikelnummer")
    benutzername = models.CharField(max_length=50, null=True)
    # item_details = models.CharField(max_length=255, null=True)
    akkuvariante = models.CharField(max_length=255, null=True)
    mit_120_Ohm_CAN_Bus_Widerstand = models.CharField(max_length=255, null=True, choices=CAN_BUS_STATUS_CHOICES, default='Nein')
    kabelvariante = models.CharField(max_length=255, null=True)
    schnittstelle = models.CharField(max_length=255, null=True)
    masse = models.CharField(max_length=255, null=True, verbose_name="Maße")
    menge = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    original_preis = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Originalpreis")
    reduzierter_preis = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Reduzierter Preis")
    gesamt = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'Artikel im Warenkorb'
        verbose_name_plural = 'Artikel im Warenkorb'

    def __str__(self):
        return self.item_nummer

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Angebot angefordert', 'Angebot angefordert'),
        ('Bestellt', 'Bestellt'),
        ('Geliefert', 'Geliefert'),
        ('Abgesagt', 'Abgesagt'),
    ]

    order_nummer = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="Bestellnummer")
    benutzername = models.CharField(max_length=50, null=True)
    order_datum = models.DateTimeField(auto_now_add=True)
    bestelldetails = models.CharField(max_length=255, null=True)
    order_status = models.CharField(max_length=255, null=True, choices=ORDER_STATUS_CHOICES, default='Bestellt', verbose_name="Bestellstatus")

    class Meta:
        verbose_name = "Bestellung"
        verbose_name_plural = "Bestellungen"

    def update_status(self, new_status):
        """
        Update the order status and save the instance.
        """
        self.order_status = new_status
        self.save()

    def place_order(self):
        """
        Set the order status to 'Bestellt'.
        """
        self.update_status('Bestellt')

    def deliver_order(self):
        """
        Set the order status to 'Geliefert'.
        """
        self.update_status('Geliefert')

class OrderItem(models.Model):
    CAN_BUS_STATUS_CHOICES = [
        ('Ja', 'Ja'),
        ('Nein', 'Nein'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=False, verbose_name="Bestellung")
    item_nummer = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="Artikelnummer")
    benutzername = models.CharField(max_length=50, null=True)
    # item_details = models.CharField(max_length=255, null=True)
    mit_120_Ohm_CAN_Bus_Widerstand = models.CharField(max_length=255, null=True, choices=CAN_BUS_STATUS_CHOICES, default='Nein')
    akkuvariante = models.CharField(max_length=255, null=True)
    kabelvariante = models.CharField(max_length=255, null=True)
    schnittstelle = models.CharField(max_length=255, null=True)
    masse = models.CharField(max_length=255, null=True, verbose_name="Maße")
    menge = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    original_preis = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Originalpreis")
    reduzierter_preis = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Reduzierter Preis")
    gesamt = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Bestellten Artikel"
        verbose_name_plural = "Bestellte Artikel"

class PreisListe(models.Model):
    kabelvariante = models.CharField(max_length=50, null=True)
    gehause = models.CharField(max_length=50, null=True, verbose_name="Akkuvariante")
    leitung = models.CharField(max_length=50, null=True, verbose_name="Schnittstelle")
    lange = models.CharField(max_length=50, null=True, verbose_name="Länge")
    qty_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_25 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_100 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_250 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_500 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_1000 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qty_2000 = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Preis"
        verbose_name_plural = "Preisliste"

class SpezielleBestellung(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Bestellt', 'Bestellt'),
        ('Geliefert', 'Geliefert'),
        ('Abgesagt', 'Abgesagt'),
    ]
    order_nummer = models.CharField(max_length=255, primary_key=True, verbose_name="Bestellnummer")
    Ust_id = models.CharField(max_length=255, null=True)
    order_datum = models.DateTimeField(auto_now_add=True, null=True)
    Status = models.CharField(max_length=255, null=True, choices=ORDER_STATUS_CHOICES, default='InCart')
    hochgeladene_datei = models.FileField(upload_to="special_orders/", null=True, verbose_name="Hochgeladene Datei")

    class Meta:
        verbose_name = "Sonderlösung"
        verbose_name_plural = "Sonderlösungen"

    def __str__(self):
        return f"Special Order {self.order_nummer}"
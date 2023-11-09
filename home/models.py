from django.db import models

class CustomerProfile(models.Model):
    ust_id = models.CharField(max_length=50, primary_key=True)
    unternehmensname = models.CharField(max_length=255, null=True)
    land = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    email = models.EmailField()
    telefonnummer = models.CharField(max_length=20, null=True)
    ansprechpartner = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.ust_id  # or any other field to represent the object as a string

class Akkuvariante(models.Model):
    name = models.CharField(max_length=255)

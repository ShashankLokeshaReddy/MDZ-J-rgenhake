from django.db import models

class CustomerProfile(models.Model):
    ust_id = models.CharField(max_length=50, primary_key=True)
    unternehmensname = models.CharField(max_length=255)
    land = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    telefonnummer = models.CharField(max_length=20)
    ansprechpartner = models.CharField(max_length=255)

    def __str__(self):
        return self.ust_id  # or any other field to represent the object as a string

class Akkuvariante(models.Model):
    name = models.CharField(max_length=255)

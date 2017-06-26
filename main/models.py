from django.db import models
from django.core.urlresolvers import reverse


class Client(models.Model):
    business_name = models.CharField(max_length=60, verbose_name="Nombre Comercial")
    first_name = models.CharField(max_length=20, verbose_name="Nombre")
    last_name = models.CharField(max_length=40, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    alt_phone = models.CharField(max_length=40, verbose_name="Telefono Alternativo")
    active = models.BooleanField(default=True, verbose_name="Activo")
    note = models.TextField(blank=True, null=True, verbose_name="Notas")

    def get_absolute_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' [' + self.business_name + ']'


class Brand(models.Model):
    brand_name = models.CharField(max_length=20, verbose_name="Marca")

    def get_absolute_url(self):
        return reverse('main:brand-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.brand_name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="Marca")
    model_name = models.CharField(max_length=20, verbose_name="Modelo")

    def get_absolute_url(self):
        return reverse('main:model-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.brand.brand_name + ' - ' + self.model_name


class Vehicle(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    licence_plate = models.CharField(max_length=20, verbose_name="Patente")
    color = models.CharField(max_length=20, verbose_name="Color")
    year = models.CharField(max_length=20, verbose_name="Año")
    model = models.ForeignKey(Model, on_delete=models.PROTECT, verbose_name="Modelo")
    transmission = models.CharField(max_length=20, verbose_name="Transmisión")

    def get_absolute_url(self):
        return reverse('main:vehicle-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.model.model_name + ' - ' + self.model.brand.brand_name + ' ' + self.color
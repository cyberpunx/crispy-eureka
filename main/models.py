# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
import dbsettings


class ClientManager(models.Manager):
    def active(self):
        return self.get(active=True)

    def inactive(self):
        return self.get(active=False)


class Client(models.Model):
    business_name = models.CharField(max_length=60, verbose_name="Nombre Comercial")
    first_name = models.CharField(max_length=20, verbose_name="Nombre")
    last_name = models.CharField(max_length=40, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    alt_phone = models.CharField(blank=True, null=True, max_length=40, verbose_name="Telefono Alternativo")
    active = models.BooleanField(default=True, verbose_name="Activo")
    note = models.TextField(blank=True, null=True, verbose_name="Notas")

    def get_absolute_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' [' + self.business_name + ']'

    objects = ClientManager()
    # usage: Client.objects.active() / Client.objects.inactive()


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


class Category(models.Model):
    category_name = models.CharField(max_length=40, verbose_name="Categoría")
    description = models.CharField(blank=True, max_length=140, verbose_name="Descripción")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoría")
    subcategory_name = models.CharField(max_length=40, verbose_name="Subcategoría")
    description = models.CharField(blank=True, max_length=140, verbose_name="Descripción")

    def __str__(self):
        return self.category.category_name + ' / ' + self.subcategory_name


class Employee(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Nombre")
    last_name = models.CharField(max_length=40, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Status(models.Model):
    STATUS_CHOICES = (
        ('PRE', 'Presupuesto'),
        ('ABI', 'Abierta'),
        ('PRO', 'En Progreso'),
        ('PAU', 'Pausada'),
        ('COM', 'Completa'),
        ('CER', 'Cerrada'),
        ('CAN', 'Cancelada'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name="Estado")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Empleado")
    date = models.DateTimeField(auto_now=True)


class Global(dbsettings.Group):
    labor_rate = dbsettings.PositiveIntegerValue(default='0', help_text='Valor de la hora de trabajo')


class WorkOrder(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name="Vehiculo")
    #status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Estado")
    STATUS_CHOICES = (
        ('PRE', 'Presupuesto'),
        ('ABI', 'Abierta'),
        ('PRO', 'En Progreso'),
        ('PAU', 'Pausada'),
        ('COM', 'Completa'),
        ('CER', 'Cerrada'),
        ('CAN', 'Cancelada'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name="Estado")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Empleado", default='')
    date = models.DateField(auto_now=True)
    note = models.CharField(blank=True, max_length=140, verbose_name="Observaciones")
    total = models.FloatField(blank=True, default=0, verbose_name="Total")

    settings = Global('Global Settings')


class Part(models.Model):
    part_name = models.CharField(max_length=40, verbose_name="Repuesto")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="SubCategoría")
    price = models.FloatField(verbose_name="Precio")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")


class Work(models.Model):
    work_name = models.CharField(max_length=40, verbose_name="Trabajo")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="SubCategoría")
    time_required = models.IntegerField(verbose_name="Tiempo")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")

#     def work_price(self):
#         if not self.time_required:
#             self.time_required = 1
#         return str(self.time_required * int(Config.labor_rate()))
#
#
# class Config(models.Model):
#     SECTION_CHOICES = (
#         ('GLOBAL', 'Global'),
#     )
#     TYPE_CHOICES = (
#         ('INT', 'INT'),
#         ('CHAR', 'CHAR'),
#     )
#     section = models.CharField(max_length=20, choices=SECTION_CHOICES, verbose_name="Sección")
#     key = models.CharField(max_length=20, verbose_name="Clave")
#     value = models.CharField(max_length=140, verbose_name="Valor")
#     type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Tipo")
#
#     def labor_rate():
#         return Config.objects.values_list('value', flat=True).get(pk=1)





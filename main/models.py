from django.db import models
from django.core.urlresolvers import reverse


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


class Class(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoría", default='')
    class_name = models.CharField(max_length=40, verbose_name="Clase")
    description = models.CharField(blank=True, max_length=140, verbose_name="Descripción")

    def __str__(self):
        return self.category.category_name + ' - ' + self.class_name


class Employee(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Nombre")
    last_name = models.CharField(max_length=40, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    active = models.BooleanField(default=True, verbose_name="Activo")


class WorkOrder(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name="Vehiculo")
    note = models.CharField(blank=True, max_length=140, verbose_name="Notas")


class Part(models.Model):
    part_name = models.CharField(max_length=40, verbose_name="Repuesto")
    belongs_to_class = models.ForeignKey(Class, on_delete=models.PROTECT, verbose_name="Clase")
    price = models.FloatField(verbose_name="Precio")
    cost = models.FloatField(verbose_name="Costo")
    provider = models.CharField(blank=True, max_length=140, verbose_name="Proveedores")
    description = models.CharField(blank=True, max_length=140, verbose_name="Descripción")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio", default='')


class Labor(models.Model):
    labor_name = models.CharField(max_length=40, verbose_name="Trabajo")
    belongs_to_class = models.ForeignKey(Class, on_delete=models.PROTECT, verbose_name="Clase")
    time_required = models.IntegerField(verbose_name="Tiempo")
    description = models.CharField(blank=True, max_length=140, verbose_name="Descripción")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio", default='')

    def labor_price(self):
        if not(self.time_required):
            self.time_required=1
        return str(self.time_required * 700)


class Detail(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT, verbose_name="Orden de Trabajo")
    labor = models.ForeignKey(Labor, on_delete=models.PROTECT, blank=True, verbose_name="Trabajo")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, blank=True, verbose_name="Repuesto")
    quantity = models.IntegerField(verbose_name="Cantidad")



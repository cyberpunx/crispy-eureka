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
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    alt_phone = models.CharField(blank=True, null=True, max_length=40, verbose_name="Telefono Alternativo")
    cuit = models.CharField(blank=True, null=True, max_length=40, verbose_name="CUIT")
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
    engine = models.CharField(max_length=20, verbose_name="Motor")
    kilometers = models.IntegerField(verbose_name="Kilometraje")
    note = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    vin = models.CharField(blank=True, null=True,max_length=20, verbose_name="Nro. Serie")
    engine_number = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Motor")

    def get_absolute_url(self):
        return reverse('main:vehicle-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name + ' [' + self.client.business_name + '] ' + \
               self.model.model_name + ' - ' + self.model.brand.brand_name + ' / ' + \
               self.color + ' / Patente: ' + self.licence_plate


class Category(models.Model):
    category_name = models.CharField(max_length=40, verbose_name="Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoría")
    subcategory_name = models.CharField(max_length=40, verbose_name="Subcategoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

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
        ('REV', 'Revisión Inicial'),
        ('ING', 'Esperando Ingreso'),
        ('ABI', 'Abierta'),
        ('INI', 'Iniciada'),
        ('REP', 'Esperando repuestos'),
        ('RET', 'Esperando Retiro'),
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
        ('REV', 'Revisión Inicial'),
        ('ING', 'Esperando Ingreso'),
        ('ABI', 'Abierta'),
        ('INI', 'Iniciada'),
        ('REP', 'Esperando repuestos'),
        ('PAU', 'Pausada'),
        ('RET', 'Esperando Retiro'),
        ('COM', 'Completa'),
        ('CER', 'Cerrada'),
        ('CAN', 'Cancelada'),
    )
    FUEL_CHOICES = (
        ('EMPTY', 'Vacío'),
        ('1/4', '1/4'),
        ('1/2', '1/2'),
        ('3/4', '3/4'),
        ('FULL', 'Lleno'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name="Estado")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Empleado", default='')
    date = models.DateTimeField(auto_now=True)
    date_in = models.DateField(blank=True, null=True, verbose_name="Fecha Entrada")
    date_out = models.DateField(blank=True, null=True, verbose_name="Fecha Salida")
    note = models.CharField(blank=True, max_length=140, verbose_name="Observaciones")
    initial_obs = models.TextField(blank=True, null=True, verbose_name="Observaciones Iniciales")
    diagnostic = models.TextField(blank=True, null=True, verbose_name="Diagnóstico")
    fuel_level = models.CharField(max_length=10, choices=FUEL_CHOICES, verbose_name="Nivel combustible")

    @property
    def total(self):
        return self.work_sum + self.part_sum

    @property
    def work_sum(self):
        work_sum = 0
        for work in self.work_set.all():
            work_sum = work_sum + work.time_required
        return work_sum * WorkOrder.settings.labor_rate

    @property
    def part_sum(self):
        part_sum = 0
        for part in self.part_set.all():
            part_sum = part_sum + part.part_price
        return part_sum

    @property
    def labor_rate(self):
        return WorkOrder.settings.labor_rate

    settings = Global('Global Settings')


class Part(models.Model):
    part_name = models.CharField(max_length=40, verbose_name="Repuesto")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="SubCategoría")
    price = models.FloatField(verbose_name="Precio")
    quantity = models.IntegerField(default=1, verbose_name="Cantidad")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")

    @property
    def part_price(self):
        return self.quantity * self.price


class Work(models.Model):
    work_name = models.CharField(max_length=40, verbose_name="Trabajo")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="SubCategoría")
    time_required = models.IntegerField(verbose_name="Tiempo")
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")

    @property
    def labor_rate(self):
        return WorkOrder.settings.labor_rate

    @property
    def work_price(self):
        return self.time_required * WorkOrder.settings.labor_rate






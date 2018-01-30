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
    id = models.AutoField(verbose_name="Nro. Cliente", primary_key=True)
    business_name = models.CharField(blank=True, max_length=60, verbose_name="Nombre Comercial")
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
        if self.business_name:
            return str(self.id) +' [' + self.business_name + ']' + self.first_name + ' ' + self.last_name
        else:
            return str(self.id) + ' / ' + self.first_name + ' ' + self.last_name

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
    color = models.CharField(blank=True, null=True, max_length=20, verbose_name="Color")
    year = models.CharField(blank=True, null=True, max_length=20, verbose_name="Año")
    model = models.ForeignKey(Model, on_delete=models.PROTECT, verbose_name="Modelo")
    engine = models.CharField(max_length=20, verbose_name="Motor")
    kilometers = models.IntegerField(blank=True, null=True, verbose_name="Kilometraje")
    note = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    vin = models.CharField(blank=True, null=True,max_length=20, verbose_name="Nro. Serie")
    engine_number = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Motor")

    def get_absolute_url(self):
        return reverse('main:vehicle-detail', kwargs={'pk': self.pk})

    def __str__(self):
        client_id = str(self.client.id)
        first_name = self.client.first_name
        last_name = self.client.last_name
        model_name = self.model.model_name
        brand_name = self.model.brand.brand_name
        licence_plate = self.licence_plate
        if (self.client.business_name):
            business_name = self.client.business_name
        else:
            business_name = ""

        if (self.color):
            color = self.color
        else:
            color = "No Color"

        if self.client.business_name:
            return client_id + ' ' + first_name + ' ' + last_name + ' [' + business_name + '] / ' + \
                    model_name + ' - ' + brand_name + ' / ' + color + ' / Patente: ' + licence_plate
        else:
            return client_id + ' ' + first_name + ' ' + last_name + ' / ' + model_name + ' - ' + brand_name + ' / ' + \
                   color + ' / Patente: ' + licence_plate


class WorkCategory(models.Model):
    category_name = models.CharField(max_length=40, verbose_name="Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.category_name

class PartCategory(models.Model):
    category_name = models.CharField(max_length=40, verbose_name="Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.category_name

class Employee(models.Model):
    display_name = models.CharField(max_length=20, verbose_name="Código", unique=True)
    first_name = models.CharField(max_length=20, verbose_name="Nombre")
    last_name = models.CharField(max_length=40, verbose_name="Apellido")
    email = models.EmailField(blank=True, unique=True, verbose_name="Email")
    phone = models.CharField(max_length=40, verbose_name="Telefono")
    active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.display_name


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

class Part(models.Model):
    part_name = models.CharField(max_length=40, verbose_name="Repuesto")
    code = models.CharField(max_length=6, verbose_name="Código", blank=True, null=True, unique=True)
    category = models.ForeignKey(PartCategory, on_delete=models.PROTECT, verbose_name="Categoría", default='')

    def __str__(self):
        if self.code:
            return '['+self.code+'] ' + self.category.category_name + ' / ' + self.part_name
        else:
            return self.category.category_name + ' / ' + self.part_name

class Work(models.Model):
    work_name = models.CharField(max_length=40, verbose_name="Trabajo")
    code = models.CharField(max_length=6, verbose_name="Código", blank=True, null=True, unique=True)
    category = models.ForeignKey(WorkCategory, on_delete=models.PROTECT, verbose_name="Categoría", default='')

    def __str__(self):
        if self.code:
            return '['+self.code+'] ' + self.category.category_name + ' / ' + self.work_name
        else:
            return self.category.category_name + ' / ' + self.work_name

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
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Empleado", default='')
    date = models.DateTimeField(auto_now=True)
    date_in = models.DateField(blank=True, null=True, verbose_name="Fecha Entrada")
    date_out = models.DateField(blank=True, null=True, verbose_name="Fecha Salida")
    note = models.CharField(blank=True, max_length=140, verbose_name="Observaciones", default='')
    initial_obs = models.TextField(blank=True, null=True, verbose_name="Observaciones Iniciales")
    diagnostic = models.TextField(blank=True, null=True, verbose_name="Diagnóstico")
    fuel_level = models.CharField(blank=True, max_length=10, choices=FUEL_CHOICES, verbose_name="Nivel combustible")
    kilometers = models.IntegerField(blank=True, null=True, verbose_name="Kilometraje")
    ticket_number = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nro. Factura")
    parts = models.ManyToManyField(Part, through='WorkorderParts')
    works = models.ManyToManyField(Work, through='WorkorderWorks')
    total_manual = models.DecimalField(blank=True, verbose_name="Total", null = True, max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.work_sum + self.part_sum

    @property
    def work_sum(self):
        work_sum = 0
        for work in self.workorderworks_set.all():
            if not work.time_required:
                time_required = 0
            else:
                time_required = work.time_required
            work_sum = work_sum + time_required
        return work_sum * WorkOrder.settings.labor_rate

    @property
    def part_sum(self):
        part_sum = 0
        for part in self.workorderparts_set.all():
            if not part.price:
                part_price = 0
            else:
                part_price = part.price * part.quantity
            part_sum = part_sum + part_price
        return part_sum

    @property
    def labor_rate(self):
        return WorkOrder.settings.labor_rate

    settings = Global('Global Settings')

class WorkorderParts(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")
    part = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name="Repuesto")
    price = models.DecimalField(blank=True, verbose_name="Precio", null = True, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(blank=True, default=1, verbose_name="Cantidad")

    @property
    def part_price(self):
        if not self.price:
            return 0
        else:
            return self.quantity * self.price

class WorkorderWorks(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name="Trabajo")
    time_required = models.DecimalField(blank=True, verbose_name="Tiempo", null = True, max_digits=5, decimal_places=1)

    @property
    def labor_rate(self):
        return WorkOrder.settings.labor_rate

    @property
    def work_price(self):
        if not self.time_required:
            return 0
        else:
            return self.time_required * WorkOrder.settings.labor_rate







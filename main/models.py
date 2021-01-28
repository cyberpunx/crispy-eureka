# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta
import dbsettings
import datetime
from django.utils import timezone
from jsignature.fields import JSignatureField


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

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.pk})

    def __str__(self):
        if self.business_name:
            return str(self.id) + ' [' + self.business_name + ']' + self.first_name + ' ' + self.last_name
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
    vin = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Serie")
    engine_number = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Motor")
    active = models.BooleanField(default=True, verbose_name="Activo")

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=20, verbose_name="Código", unique=True)
    phone = models.CharField(max_length=40, verbose_name="Telefono")

    def __str__(self):
        return self.display_name


class Global(dbsettings.Group):
    labor_rate = dbsettings.PositiveIntegerValue(default='0', help_text='Valor de la hora de trabajo')
    texto_firma_entrada = dbsettings.StringValue(default='', help_text='Texto de firma al ingresar vehículo',
                                                 widget=forms.Textarea, required=False)
    texto_firma_salida = dbsettings.StringValue(default='', help_text='Texto de firma al salir vehículo',
                                                widget=forms.Textarea, required=False)


class Part(models.Model):
    part_name = models.CharField(max_length=40, verbose_name="Repuesto")
    code = models.CharField(max_length=6, verbose_name="Código", blank=True, null=True, unique=True)
    category = models.ForeignKey(PartCategory, on_delete=models.PROTECT, verbose_name="Categoría", default='')

    def __str__(self):
        if self.code:
            return '[' + self.code + '] ' + self.category.category_name + ' / ' + self.part_name
        else:
            return self.category.category_name + ' / ' + self.part_name


class Work(models.Model):
    work_name = models.CharField(max_length=40, verbose_name="Trabajo")
    code = models.CharField(max_length=6, verbose_name="Código", blank=True, null=True, unique=True)
    category = models.ForeignKey(WorkCategory, on_delete=models.PROTECT, verbose_name="Categoría", default='')

    def __str__(self):
        if self.code:
            return '[' + self.code + '] ' + self.category.category_name + ' / ' + self.work_name
        else:
            return self.category.category_name + ' / ' + self.work_name


class WorkOrder(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name="Vehiculo")
    FUEL_CHOICES = (
        ('EMPTY', 'Vacío'),
        ('1/4', '1/4'),
        ('1/2', '1/2'),
        ('3/4', '3/4'),
        ('FULL', 'Lleno'),
    )
    note = models.CharField(blank=True, max_length=140, verbose_name="Notas", default='')
    initial_obs = models.TextField(blank=True, null=True, verbose_name="Observaciones Iniciales")
    diagnostic = models.TextField(blank=True, null=True, verbose_name="Diagnóstico")
    fuel_level = models.CharField(blank=True, max_length=10, choices=FUEL_CHOICES, verbose_name="Nivel combustible")
    kilometers = models.IntegerField(blank=True, null=True, verbose_name="Kilometraje")
    ticket_number = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nro. Factura")
    parts = models.ManyToManyField(Part, through='WorkorderParts')
    works = models.ManyToManyField(Work, through='WorkorderWorks')
    total_manual = models.DecimalField(blank=True, verbose_name="Sobreescribir Total", null=True, max_digits=10,
                                       decimal_places=2)
    firma_entrada = JSignatureField(blank=True, null=True, verbose_name="Firma ingreso a taller")
    firma_salida = JSignatureField(blank=True, null=True, verbose_name="Firma salida de taller")
    firma_texto_entrada = models.CharField(blank=True, null=True, verbose_name="Texto de Firma ingreso a taller",
                                           max_length=256)
    firma_texto_salida = models.CharField(blank=True, null=True, verbose_name="Texto de Firma salida de taller",
                                          max_length=256)

    # DATOS QUE SE PERISTEN JUNTO CON LA ORDEN PARA "CONGELARLOS" EN EL TIEMPO
    vehicle_licence_plate = models.CharField(blank=True, null=True, max_length=20, verbose_name="Patente")
    vehicle_color = models.CharField(blank=True, null=True, max_length=20, verbose_name="Color")
    vehicle_year = models.CharField(blank=True, null=True, max_length=20, verbose_name="Año")
    vehicle_model = models.CharField(blank=True, null=True, max_length=60, verbose_name="Modelo")
    vehicle_engine = models.CharField(blank=True, null=True, max_length=20, verbose_name="Motor")
    vehicle_vin = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Serie")
    vehicle_engine_number = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nro. Motor")

    client_id = models.CharField(blank=True, null=True, max_length=10, verbose_name="Nro. Cliente")
    client_business_name = models.CharField(blank=True, null=True,max_length=60, verbose_name="Nombre Comercial")
    client_first_name = models.CharField(blank=True, null=True, max_length=20, verbose_name="Nombre")
    client_last_name = models.CharField(blank=True, null=True, max_length=40, verbose_name="Apellido")
    client_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    client_phone = models.CharField(blank=True, null=True, max_length=40, verbose_name="Telefono")
    client_alt_phone = models.CharField(blank=True, null=True, max_length=40, verbose_name="Telefono Alternativo")
    client_cuit = models.CharField(blank=True, null=True, max_length=40, verbose_name="CUIT")

    def save(self, *args, **kwargs):
        self.vehicle_licence_plate = self.vehicle.licence_plate
        self.vehicle_color = self.vehicle.color
        self.vehicle_year = self.vehicle.year
        self.vehicle_model = str(self.vehicle.model.brand.brand_name) + ' ' + str(self.vehicle.model.model_name)
        self.vehicle_engine = self.vehicle.engine
        self.vehicle_vin = self.vehicle.vin
        self.vehicle_engine_number = self.vehicle.engine_number

        self.client_id = self.vehicle.client.id
        self.client_business_name = self.vehicle.client.business_name
        self.client_first_name = self.vehicle.client.first_name
        self.client_last_name = self.vehicle.client.last_name
        self.client_email = self.vehicle.client.email
        self.client_phone = self.vehicle.client.phone
        self.client_alt_phone = self.vehicle.client.alt_phone
        self.client_cuit = self.vehicle.client.cuit
        return super(WorkOrder, self).save(*args, **kwargs)

    @property
    def last_movement(self):
        last_movement = Movement.objects.filter(work_order__id__exact=self.id).order_by('-id')[:1].first()
        return last_movement

    @property
    def first_movement(self):
        first_movement = Movement.objects.filter(work_order__id__exact=self.id).order_by('id')[:1].first()
        return first_movement

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
    price = models.DecimalField(blank=True, verbose_name="Precio", null=True, max_digits=10, decimal_places=2)
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
    time_required = models.DecimalField(blank=True, verbose_name="Tiempo", null=True, max_digits=5, decimal_places=1)

    @property
    def labor_rate(self):
        return WorkOrder.settings.labor_rate

    @property
    def work_price(self):
        if not self.time_required:
            return 0
        else:
            return self.time_required * WorkOrder.settings.labor_rate


class Movement(models.Model):
    STATUS_CHOICES = (
        ('Abierta', 'Abierta'),
        ('En Progreso', 'En Progreso'),
        ('Esperando repuestos', 'Esperando repuestos'),
        ('Pausada', 'Pausada'),
        ('Completa', 'Completa'),
        ('Cerrada', 'Cerrada'),
        ('Cancelada', 'Cancelada'),
        ('Presupuesto', 'Presupuesto'),
    )
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0],
                              verbose_name="Estado", blank=False)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")
    date = models.DateField(verbose_name="Fecha", blank=True)
    time = models.TimeField(verbose_name="Hora", blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Empleado")
    note = models.CharField(blank=True, max_length=140, verbose_name="Observaciones", default='')

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()
        if not self.time:
            self.time = datetime.datetime.now()
        return super(Movement, self).save(*args, **kwargs)


class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name="Orden de Servicio")
    start_time = models.DateTimeField(verbose_name="Inicio", auto_now=True)
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="Fin")

    @property
    def is_running(self):
        if self.start_time:
            if self.end_time:
                return False
            else:
                return True

    @property
    def total_time(self):
        if self.start_time:
            if self.end_time:
                dt = self.end_time - self.start_time
                seconds = dt.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                return datetime.timedelta(hours=hours, minutes=minutes, seconds=round(seconds, 0))
            else:
                return 0

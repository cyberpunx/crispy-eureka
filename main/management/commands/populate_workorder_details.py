from django.core.management.base import BaseCommand, CommandError
from main.models import Vehicle, Client, WorkOrder, Model


class Command(BaseCommand):
    help = 'Copia datos de Vehiculo y Cliente a cada fila de Workorder'

    def handle(self, *args, **options):
        orders = WorkOrder.objects.all()
        for order in orders:
            order.vehicle_licence_plate = order.vehicle.licence_plate
            order.vehicle_color = order.vehicle.color
            order.vehicle_year = order.vehicle.year
            order.vehicle_model = str(order.vehicle.model.brand.brand_name) + ' ' + str(order.vehicle.model.model_name)
            order.vehicle_engine = order.vehicle.engine
            order.vehicle_vin = order.vehicle.vin
            order.vehicle_engine_number = order.vehicle.engine_number
            order.client_id = order.vehicle.client.id
            order.client_business_name = order.vehicle.client.business_name
            order.client_first_name = order.vehicle.client.first_name
            order.client_last_name = order.vehicle.client.last_name
            order.client_email = order.vehicle.client.email
            order.client_phone = order.vehicle.client.phone
            order.client_alt_phone = order.vehicle.client.alt_phone
            order.client_cuit = order.vehicle.client.cuit
            order.save()

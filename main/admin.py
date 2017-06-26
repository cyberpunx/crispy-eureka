from django.contrib import admin
from .models import Client, Brand, Model, Vehicle

admin.site.register(Client)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Vehicle)


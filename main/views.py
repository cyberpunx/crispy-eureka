from django.shortcuts import render
from .models import Client, Vehicle, Model, Brand
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index_view(request):
    return render(request, 'main/index.html', {})


class ClientIndexView(generic.ListView):
    template_name = 'main/client/index.html'

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailView(generic.DetailView):
    template_name = 'main/client/detail.html'
    model = Client


class ClientCreateView(CreateView):
    template_name = 'main/client/client_form.html'
    model = Client
    fields = ['business_name', 'first_name', 'last_name', 'email', 'phone', 'alt_phone', 'active', 'note']


class ClientUpdateView(UpdateView):
    template_name = 'main/client/client_form.html'
    model = Client
    fields = ['business_name', 'first_name', 'last_name', 'email', 'phone', 'alt_phone', 'active', 'note']


class ClientDeleteView(DeleteView):
    template_name = 'main/client/confirm_delete.html'
    model = Client
    success_url = reverse_lazy('main:client-index')


class VehicleIndexView(generic.ListView):
    template_name = 'main/vehicle/index.html'

    def get_queryset(self):
        return Vehicle.objects.all()


class VehicleCreateView(CreateView):
    template_name = 'main/vehicle/vehicle_form.html'
    model = Vehicle
    fields = ['licence_plate', 'color', 'year', 'model', 'transmission', 'client']


class VehicleUpdateView(UpdateView):
    template_name = 'main/vehicle/vehicle_form.html'
    model = Vehicle
    fields = ['licence_plate', 'color', 'year', 'model', 'transmission', 'client']


class VehicleDeleteView(DeleteView):
    template_name = 'main/vehicle/confirm_delete.html'
    model = Vehicle
    success_url = reverse_lazy('main:vehicle-index')


class BrandIndexView(generic.ListView):
    template_name = 'main/brand/index.html'

    def get_queryset(self):
        return Brand.objects.all()


class BrandCreateView(CreateView):
    template_name = 'main/brand/brand_form.html'
    model = Brand
    fields = ['brand_name']


class ModelIndexView(generic.ListView):
    template_name = 'main/model/index.html'

    def get_queryset(self):
        return Model.objects.all()


class ModelCreateView(CreateView):
    template_name = 'main/model/model_form.html'
    model = Model
    fields = ['model_name', 'brand']
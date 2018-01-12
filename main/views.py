# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Client, Vehicle, Model, Brand, WorkCategory, PartCategory, Employee, WorkOrder, Work, Part
from dal import autocomplete
from main import models
from .forms import VehicleForm, WorkOrderForm, WorkForm, PartForm
from django.views import generic
from django.db.models import Sum
from django.core.urlresolvers import reverse_lazy, reverse
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

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(UpdateView):
    template_name = 'main/client/client_form.html'
    model = Client
    fields = ['business_name', 'first_name', 'last_name', 'email', 'phone', 'alt_phone', 'active', 'note']

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    template_name = 'main/client/confirm_delete.html'
    model = Client
    success_url = reverse_lazy('main:client-index')


class VehicleIndexView(generic.ListView):
    template_name = 'main/vehicle/index.html'

    def get_queryset(self):
        return Vehicle.objects.all()


class VehicleCreateView(CreateView):
    template_name = 'main/vehicle/autocomplete_form.html'
    form_class = VehicleForm
    model = Vehicle

    def form_valid(self, form):
        form.instance.client_id = self.kwargs.get('pk')
        return super(VehicleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.client.pk})


class VehicleUpdateView(UpdateView):
    template_name = 'main/vehicle/autocomplete_form.html'
    model = Vehicle
    form_class = VehicleForm

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.client.pk})


class VehicleDeleteView(DeleteView):
    template_name = 'main/vehicle/confirm_delete.html'
    model = Vehicle

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.client.pk})


class BrandIndexView(generic.ListView):
    template_name = 'main/brand/index.html'

    def get_queryset(self):
        return Brand.objects.all()


class BrandCreateView(CreateView):
    template_name = 'main/brand/brand_form.html'
    model = Brand
    fields = ['brand_name']
    success_url = reverse_lazy('main:brand-index')


class ModelIndexView(generic.ListView):
    template_name = 'main/model/index.html'

    def get_queryset(self):
        return Model.objects.all()


class ModelCreateView(CreateView):
    template_name = 'main/model/model_form.html'
    model = Model
    fields = ['model_name', 'brand']
    success_url = reverse_lazy('main:model-index')


class WorkCategoryIndexView(generic.ListView):
    template_name = 'main/workcategory/index.html'

    def get_queryset(self):
        return WorkCategory.objects.all()


class WorkCategoryCreateView(CreateView):
    template_name = 'main/workcategory/workcategory_form.html'
    model = WorkCategory
    fields = ['category_name', 'description']
    success_url = reverse_lazy('main:workcategory-index')

class PartCategoryIndexView(generic.ListView):
    template_name = 'main/partcategory/index.html'

    def get_queryset(self):
        return PartCategory.objects.all()


class PartCategoryCreateView(CreateView):
    template_name = 'main/partcategory/partcategory_form.html'
    model = PartCategory
    fields = ['category_name', 'description']
    success_url = reverse_lazy('main:partcategory-index')

class EmployeeIndexView(generic.ListView):
    template_name = 'main/employee/index.html'

    def get_queryset(self):
        return Employee.objects.all()


class EmployeeDetailView(generic.DetailView):
    template_name = 'main/employee/detail.html'
    model = Employee


class EmployeeCreateView(CreateView):
    template_name = 'main/employee/employee_form.html'
    model = Employee
    fields = ['display_name', 'first_name', 'last_name', 'email', 'phone', 'active']
    success_url = reverse_lazy('main:employee-index')


class EmployeeUpdateView(UpdateView):
    template_name = 'main/employee/employee_form.html'
    model = Employee
    fields = ['display_name', 'first_name', 'last_name', 'email', 'phone', 'active']
    success_url = reverse_lazy('main:employee-index')


class EmployeeDeleteView(DeleteView):
    template_name = 'main/employee/confirm_delete.html'
    model = Employee
    success_url = reverse_lazy('main:employee-index')


class WorkOrderIndexView(generic.ListView):
    template_name = 'main/workorder/index.html'

    def get_queryset(self):
        return WorkOrder.objects.all()

    def get_context_data(self, **kwargs):
        context = super(WorkOrderIndexView, self).get_context_data(**kwargs)
        context['labor_rate'] = models.WorkOrder.settings.labor_rate
        return context


class WorkOrderDetailView(generic.DetailView):
    template_name = 'main/workorder/detail.html'
    model = WorkOrder

class WorkOrderPrintView(generic.DetailView):
    template_name = 'main/workorder/print.html'
    model = WorkOrder


class WorkOrderDeleteView(DeleteView):
    template_name = 'main/workorder/confirm_delete.html'
    model = WorkOrder
    success_url = reverse_lazy('main:workorder-index')


class WorkOrderUpdateView(UpdateView):
    template_name = 'main/workorder/workorder_form.html'
    model = WorkOrder
    form_class = WorkOrderForm

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.pk})


class WorkOrderCreateView(CreateView):
    template_name = 'main/workorder/autocomplete_form.html'
    model = WorkOrder
    form_class = WorkOrderForm
    success_url = reverse_lazy('main:workorder-index')

class WorkCreateView(CreateView):
    template_name = 'main/work/autocomplete_form.html'
    model = Work
    form_class = WorkForm

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs.get('pk')
        return super(WorkCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})

class WorkUpdateView(UpdateView):
    template_name = 'main/work/work_form.html'
    model = Work
    fields = ['work_name', 'category', 'time_required']

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})


class WorkDeleteView(DeleteView):
    template_name = 'main/work/confirm_delete.html'
    model = Work

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})

class PartCreateView(CreateView):
    template_name = 'main/part/autocomplete_form.html'
    model = Part
    form_class = PartForm

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs.get('pk')
        return super(PartCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})

class PartUpdateView(UpdateView):
    template_name = 'main/part/part_form.html'
    model = Part
    fields = ['part_name', 'category', 'price']

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})


class PartDeleteView(DeleteView):
    template_name = 'main/part/confirm_delete.html'
    model = Part

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})


# ---------------------- AUTOCOMPLETE VIEWS ---------------------- #


class ModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Model.objects.none()

        qs = Model.objects.all()

        if self.q:
            qs = qs.filter(brand__brand_name__istartswith=self.q) | qs.filter(model_name__istartswith=self.q)

        return qs


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Client.objects.none()

        qs = Client.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q) | qs.filter(last_name__istartswith=self.q) \
                 | qs.filter(business_name__istartswith=self.q)

        return qs


class VehicleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = Vehicle.objects.all()

        if self.q:
            qs = qs.filter(client__first_name__istartswith=self.q) | qs.filter(client__last_name__istartswith=self.q) \
                 | qs.filter(client__business_name__istartswith=self.q) \
                 | qs.filter(model__model_name__istartswith=self.q) \
                 | qs.filter(model__brand_brand_name__istartswith=self.q)

        return qs

class WorkCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = WorkCategory.objects.all()

        if self.q:
            qs = qs.filter(category_name__icontains=self.q)

        return qs

class PartCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = PartCategory.objects.all()

        if self.q:
            qs = qs.filter(category_name__icontains=self.q)

        return qs
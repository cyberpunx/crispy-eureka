# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .models import Client, Vehicle, Model, Brand, WorkCategory, PartCategory, Employee, WorkOrder, Work, Part, WorkorderParts, WorkorderWorks, Movement, Timer
from django.contrib.auth.models import User
from dal import autocomplete
from main import models
from .forms import VehicleForm, VehicleClientForm, WorkOrderForm, WorkOrderUpdateForm, WorkOrderUpdateDetailsForm, WorkForm, PartForm, WorkorderPartsForm, WorkorderWorksForm, MovementForm, EmployeeCreateForm
from django.views import generic
from django.db.models import Sum
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from main.decorators import staff_required
import datetime

def index_view(request):
    return render(request, 'main/index.html', {})

def welcome_view(request):
    return render(request, 'main/welcome.html', {})

class ProfileView(TemplateView):
    template_name = "main/user/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        workorders = WorkOrder.objects.all()
        timers = Timer.objects.filter(user__id=self.request.user.id).order_by('-id')
        last_timer = Timer.objects.filter(user__id=self.request.user.id).order_by('-id')[:1].first()
        context['workorders'] = workorders
        context['timers'] = timers
        context['last_timer'] = last_timer
        return context

def timer_create_view(request, pk):
    timer = Timer(user = request.user, work_order =  WorkOrder.objects.get(pk=pk), start_time=datetime.datetime.now())
    timer.save()
    return redirect('main:profile')

def timer_stop_view(request, pk):
    timer = Timer.objects.get(pk=pk)
    timer.end_time = datetime.datetime.now()
    timer.save()
    return redirect('main:profile')

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

class ClientHistoryView(generic.ListView):
    template_name = 'main/workorder/index.html'

    def get_queryset(self):
        qs = WorkOrder.objects.get_queryset().order_by('id')
        qs = qs.filter(vehicle__client__id__exact=self.kwargs['pk'])
        return qs

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

class VehicleClientCreateView(CreateView):
    template_name = 'main/vehicle/autocomplete_form.html'
    form_class = VehicleClientForm
    model = Vehicle

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

class VehicleHistoryView(generic.ListView):
    template_name = 'main/workorder/index.html'

    def get_queryset(self):
        qs = WorkOrder.objects.get_queryset().order_by('id')
        qs = qs.filter(vehicle__id__exact=self.kwargs['pk'])
        return qs

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

class WorkCategoryDeleteView(DeleteView):
    template_name = 'main/workcategory/confirm_delete.html'
    model = WorkCategory
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

class PartCategoryDeleteView(DeleteView):
    template_name = 'main/partcategory/confirm_delete.html'
    model = PartCategory
    success_url = reverse_lazy('main:partcategory-index')

class EmployeeIndexView(generic.ListView):
    template_name = 'main/employee/index.html'
    model = User

    def get_queryset(self):
        return User.objects.all()


class EmployeeDetailView(generic.DetailView):
    template_name = 'main/employee/detail.html'
    model = Employee


class EmployeeCreateView(CreateView):
    template_name = 'main/employee/employee_form.html'
    model = User
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('main:employee-index')

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        return redirect('main:employee-index')


class EmployeeUpdateView(UpdateView):
    template_name = 'main/employee/employee_form.html'
    model = User
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('main:employee-index')

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        return redirect('main:employee-index')


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

    def get_context_data(self, **kwargs):
        context = super(WorkOrderDetailView, self).get_context_data(**kwargs)
        last_status = Movement.objects.filter(work_order__id__exact=self.kwargs['pk']).order_by('-id')[:1].first()
        context['status'] = last_status
        return context

class WorkOrderUserDetailView(generic.DetailView):
    template_name = 'main/user/workorder_detail.html'
    model = WorkOrder

    def get_context_data(self, **kwargs):
        context = super(WorkOrderUserDetailView, self).get_context_data(**kwargs)
        last_status = Movement.objects.filter(work_order__id__exact=self.kwargs['pk']).order_by('-id')[:1].first()
        context['status'] = last_status
        return context

class WorkOrderPrintView(generic.DetailView):
    template_name = 'main/workorder/print.html'
    model = WorkOrder


class WorkOrderDeleteView(DeleteView):
    template_name = 'main/workorder/confirm_delete.html'
    model = WorkOrder
    success_url = reverse_lazy('main:workorder-index')


class WorkOrderUpdateView(UpdateView):
    template_name = 'main/workorder/workorder_update.html'
    model = WorkOrder
    form_class = WorkOrderUpdateForm

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.pk})

class WorkOrderUpdateDetailsView(UpdateView):
    template_name = 'main/workorder/details_form.html'
    model = WorkOrder
    form_class = WorkOrderUpdateDetailsForm

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.pk})


class WorkOrderCreateView(CreateView):
    template_name = 'main/workorder/autocomplete_form.html'
    model = WorkOrder
    form_class = WorkOrderForm

    def get_success_url(self):
        return reverse('main:movements-add', kwargs={'pk': self.object.id})


class WorkCreateView(CreateView):
    template_name = 'main/work/autocomplete_form.html'
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy('main:work-index')

class WorkIndexView(generic.ListView):
    template_name = 'main/work/index.html'

    def get_queryset(self):
        return Work.objects.all()

class WorkUpdateView(UpdateView):
    template_name = 'main/work/autocomplete_form.html'
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy('main:work-index')


class WorkDeleteView(DeleteView):
    template_name = 'main/work/confirm_delete.html'
    model = Work
    success_url = reverse_lazy('main:work-index')

class WorkOrderWorksCreateView(CreateView):
    template_name = 'main/workorderworks/autocomplete_form.html'
    model = WorkorderWorks
    form_class = WorkorderWorksForm
    success_url = reverse_lazy('main:workorder-index')

    def get_context_data(self, **kwargs):
        context = super(WorkOrderWorksCreateView, self).get_context_data(**kwargs)
        qs = WorkOrder.objects.get(pk=self.kwargs['pk'])
        context['workorder_data'] = qs
        return context

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs.get('pk')
        return super(WorkOrderWorksCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:workorderworks-add', kwargs={'pk': self.object.work_order.pk})

class WorkOrderWorksDeleteView(DeleteView):
    template_name = 'main/workorderworks/confirm_delete.html'
    model = WorkorderWorks

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})

class WorkOrderWorksListDeleteView(DeleteView):
    template_name = 'main/workorderworks/confirm_listdelete.html'
    model = WorkorderWorks

    def get_success_url(self):
        return reverse('main:workorderworks-add', kwargs={'pk': self.object.work_order.pk})

class WorkOrderPartsCreateView(CreateView):
    template_name = 'main/workorderparts/autocomplete_form.html'
    model = WorkorderParts
    form_class = WorkorderPartsForm
    success_url = reverse_lazy('main:workorder-index')

    def get_context_data(self, **kwargs):
        context = super(WorkOrderPartsCreateView, self).get_context_data(**kwargs)
        qs = WorkOrder.objects.get(pk=self.kwargs['pk'])
        context['workorder_data'] = qs
        return context

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs.get('pk')
        return super(WorkOrderPartsCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:workorderparts-add', kwargs={'pk': self.object.work_order.pk})

class WorkOrderPartsDeleteView(DeleteView):
    template_name = 'main/workorderparts/confirm_delete.html'
    model = WorkorderParts

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})

class WorkOrderPartsListDeleteView(DeleteView):
    template_name = 'main/workorderparts/confirm_listdelete.html'
    model = WorkorderParts

    def get_success_url(self):
        return reverse('main:workorderparts-add', kwargs={'pk': self.object.work_order.pk})

class PartIndexView(generic.ListView):
    template_name = 'main/part/index.html'

    def get_queryset(self):
        return Part.objects.all()

class PartCreateView(CreateView):
    template_name = 'main/part/autocomplete_form.html'
    model = Part
    form_class = PartForm
    success_url = reverse_lazy('main:part-index')


class PartUpdateView(UpdateView):
    template_name = 'main/part/autocomplete_form.html'
    model = Part
    form_class = PartForm
    success_url = reverse_lazy('main:part-index')


class PartDeleteView(DeleteView):
    template_name = 'main/part/confirm_delete.html'
    model = Part
    success_url = reverse_lazy('main:part-index')


class MovementCreateView(CreateView):
    template_name = 'main/movement/movement_form.html'
    form_class = MovementForm
    model = Movement

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs.get('pk')
        return super(MovementCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:workorder-detail', kwargs={'pk': self.object.work_order.pk})


# ---------------------- AUTOCOMPLETE VIEWS ---------------------- #


class ModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Model.objects.none()

        qs = Model.objects.get_queryset().order_by('id')


        if self.q:
            qs = qs.filter(brand__brand_name__icontains=self.q) | qs.filter(model_name__icontains=self.q)

        return qs


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Client.objects.none()

        qs = Client.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(first_name__icontains=self.q) | qs.filter(last_name__icontains=self.q) \
                 | qs.filter(business_name__icontains=self.q) \
                 | qs.filter(full_name__icontains=self.q)

        return qs


class VehicleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = Vehicle.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(client__first_name__icontains=self.q) \
                 | qs.filter(client__last_name__icontains=self.q) \
                 | qs.filter(client__business_name__icontains=self.q) \
                 | qs.filter(licence_plate__icontains=self.q) \
                 | qs.filter(model__model_name__icontains=self.q) \
                 | qs.filter(model__brand__brand_name__icontains=self.q) \
                 | qs.filter(client__full_name__icontains=self.q)

        return qs

class WorkCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = WorkCategory.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(category_name__icontains=self.q)

        return qs

class PartCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = PartCategory.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(category_name__icontains=self.q)

        return qs

class PartsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = Part.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(part_name__icontains=self.q) | qs.filter(category__category_name__icontains=self.q) \
                    | qs.filter(code__icontains=self.q)

        return qs

class WorksAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vehicle.objects.none()

        qs = Work.objects.get_queryset().order_by('id')

        if self.q:
            qs = qs.filter(work_name__icontains=self.q) | qs.filter(category__category_name__icontains=self.q) \
                    | qs.filter(code__icontains=self.q)

        return qs


class CalendarView(TemplateView):
    template_name = "main/calendar.html"


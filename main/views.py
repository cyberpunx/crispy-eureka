from django.shortcuts import render, redirect
from .models import Client, Vehicle, Model, Brand, Category, Class, Employee, Labor, WorkOrder, Part
from dal import autocomplete
from .forms import VehicleForm, LaborFormSet, WorkOrderUpdateForm
from django.views import generic
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
    #template_name = 'main/vehicle/vehicle_form.html'
    #fields = ['licence_plate', 'color', 'year', 'model', 'transmission']
    template_name = 'main/vehicle/autocomplete_form.html'
    form_class = VehicleForm
    model = Vehicle

    def form_valid(self, form):
        form.instance.client_id = self.kwargs.get('pk')
        return super(VehicleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:client-detail', kwargs={'pk': self.object.client.pk})


#class VehicleUpdateView(UpdateView):
#    template_name = 'main/vehicle/vehicle_form.html'
#    model = Vehicle
#    fields = ['licence_plate', 'color', 'year', 'model', 'transmission', 'client']


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


class CategoryIndexView(generic.ListView):
    template_name = 'main/category/index.html'

    def get_queryset(self):
        return Category.objects.all()


class CategoryCreateView(CreateView):
    template_name = 'main/category/category_form.html'
    model = Category
    fields = ['category_name', 'description']
    success_url = reverse_lazy('main:category-index')


class ClassIndexView(generic.ListView):
    template_name = 'main/class/index.html'

    def get_queryset(self):
        return Class.objects.all()


class ClassCreateView(CreateView):
    template_name = 'main/class/class_form.html'
    model = Class
    fields = ['class_name', 'description', 'category']
    success_url = reverse_lazy('main:class-index')


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
    fields = ['first_name', 'last_name', 'email', 'phone', 'active']
    success_url = reverse_lazy('main:employee-index')


class EmployeeUpdateView(UpdateView):
    template_name = 'main/employee/employee_form.html'
    model = Employee
    fields = ['first_name', 'last_name', 'email', 'phone', 'active']
    success_url = reverse_lazy('main:employee-index')


class EmployeeDeleteView(DeleteView):
    template_name = 'main/employee/confirm_delete.html'
    model = Employee
    success_url = reverse_lazy('main:employee-index')


class WorkOrderIndexView(generic.ListView):
    template_name = 'main/workorder/index.html'

    def get_queryset(self):
        return WorkOrder.objects.all()


class WorkOrderCreateView(CreateView):
    template_name = 'main/workorder/workorder_form.html'
    model = WorkOrder
    success_url = reverse_lazy('main:workorder-index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(WorkOrderCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LaborFormSet(self.request.POST)
        else:
            context['formset'] = LaborFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WorkOrderUpdateView(UpdateView):
    #form_class = WorkOrderUpdateForm
    #template_name = 'main/workorder/workorder_form.html'
    template_name = 'main/workorder/workorder_template.html'
    model = WorkOrder
    success_url = reverse_lazy('main:workorder-index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(WorkOrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LaborFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = LaborFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WorkOrderDetailView(generic.DetailView):
    #form_class = WorkOrderUpdateForm
    template_name = 'main/workorder/detail.html'
    model = WorkOrder
    success_url = reverse_lazy('main:workorder-index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(WorkOrderDetailView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LaborFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = LaborFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


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
            qs = qs.filter(first_name__istartswith=self.q) | qs.filter(last_name__istartswith=self.q)

        return qs
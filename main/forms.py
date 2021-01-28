from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from .models import Vehicle, WorkOrder, Work, Part, WorkorderParts, WorkorderWorks, Movement, User, Employee
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licence_plate', 'color', 'year', 'model', 'engine', 'vin', 'engine_number', 'note']
        widgets = {
            'model': autocomplete.ModelSelect2(url='main:model-autocomplete'),
            'note': forms.Textarea()
        }


class VehicleClientForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['client', 'licence_plate', 'color', 'year', 'model', 'engine', 'vin', 'engine_number', 'note']
        widgets = {
            'client': autocomplete.ModelSelect2(url='main:client-autocomplete'),
            'model': autocomplete.ModelSelect2(url='main:model-autocomplete'),
            'note': forms.Textarea()
        }


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder

        fields = ['vehicle', 'initial_obs', 'fuel_level', 'kilometers', 'diagnostic', 'note', 'ticket_number',
                  'total_manual']
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea(),
            'date_in': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_out': forms.widgets.DateInput(attrs={'type': 'date'}),
        }


class WorkOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkOrder

        fields = ['initial_obs', 'fuel_level', 'kilometers', 'diagnostic', 'note', 'ticket_number', 'total_manual']
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea(),
            'date_in': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_out': forms.widgets.DateInput(attrs={'type': 'date'}),
        }


class WorkOrderUpdateDetailsForm(forms.ModelForm):
    class Meta:
        model = WorkOrder

        fields = ['fuel_level', 'kilometers', 'note', 'ticket_number', 'total_manual']
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea(),
            'date_in': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_out': forms.widgets.DateInput(attrs={'type': 'date'}),
        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['work_name', 'category', 'code']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:workcategory-autocomplete'),
        }


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['part_name', 'category', 'code']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:partcategory-autocomplete'),
        }


class WorkorderPartsForm(forms.ModelForm):
    class Meta:
        model = WorkorderParts
        fields = ['part', 'price', 'quantity']
        widgets = {
            'part': autocomplete.ModelSelect2(url='main:parts-autocomplete'),
        }


class WorkorderWorksForm(forms.ModelForm):
    class Meta:
        model = WorkorderWorks
        fields = ['work', 'time_required']
        widgets = {
            'work': autocomplete.ModelSelect2(url='main:works-autocomplete'),
        }


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['status', 'employee', 'date', 'time', 'note']
        widgets = {
            'date': forms.widgets.DateTimeInput(attrs={'type': 'date'}),
            'time': forms.widgets.DateTimeInput(attrs={'type': 'time'}),
            'note': forms.Textarea()
        }


MovementFormSet = inlineformset_factory(WorkOrder, Movement, form=MovementForm, extra=1)


class EmployeeCreateForm(UserCreationForm):
    display_name = forms.CharField(max_length=20, label='Código de empleado')
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    phone = forms.CharField(max_length=40, label='Teléfono')
    email = forms.EmailField(required=False, label='Email')
    is_staff = forms.BooleanField(required=False, label='Es Administrativo?')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super(EmployeeCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['is_staff']
        user.save()
        employee = Employee.objects.create(user=user)
        employee.display_name = self.cleaned_data['display_name']
        employee.phone = self.cleaned_data['phone']
        employee.save()
        return user

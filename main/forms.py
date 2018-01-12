from dal import autocomplete
from django import forms
from .models import Vehicle, WorkOrder, Work, Part


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licence_plate', 'color', 'year', 'model', 'engine', 'kilometers', 'vin', 'engine_number', 'note']
        widgets = {
            'model': autocomplete.ModelSelect2(url='main:model-autocomplete'),
            'note': forms.Textarea()
        }


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = ['vehicle', 'status', 'date_in', 'date_out', 'employee', 'initial_obs', 'fuel_level', 'diagnostic', 'note', 'ticket_number']
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea(),
            'date_in':  forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_out':  forms.widgets.DateInput(attrs={'type': 'date'}),
        }

class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ['work_name', 'category', 'time_required']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:workcategory-autocomplete'),
        }

class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ['part_name', 'category', 'price', 'quantity']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:partcategory-autocomplete'),
        }



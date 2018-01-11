from dal import autocomplete
from django import forms
from .models import Vehicle, WorkOrder, Work


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
        fields = ['vehicle', 'status', 'employee', 'initial_obs', 'fuel_level', 'diagnostic',   'note']
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea()
        }

class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ['work_name', 'subcategory', 'time_required']
        widgets = {
            'subcategory': autocomplete.ModelSelect2(url='main:subcategory-autocomplete'),
        }



from dal import autocomplete
from django import forms
from .models import Vehicle, WorkOrder


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licence_plate', 'color', 'year', 'model', 'transmission']
        widgets = {
            'model': autocomplete.ModelSelect2(url='main:model-autocomplete')
        }


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = '__all__'
        widgets = {
            'vehicle': autocomplete.ModelSelect2(url='main:vehicle-autocomplete'),
            'note': forms.Textarea()
        }



from dal import autocomplete
from django import forms
from .models import Vehicle, WorkOrder, Work, Part, WorkorderParts, WorkorderWorks


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
        fields = ['work_name', 'category']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:workcategory-autocomplete'),
        }

class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ['part_name', 'category']
        widgets = {
            'category': autocomplete.ModelSelect2(url='main:partcategory-autocomplete'),
        }

class WorkorderPartsForm(forms.ModelForm):

    class Meta:
        model = WorkorderParts
        fields = ['part', 'price', 'quantity']

class WorkorderWorksForm(forms.ModelForm):

    class Meta:
        model = WorkorderWorks
        fields = ['work', 'time_required']



from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from .models import Vehicle, WorkOrder, Labor
from crispy_forms.helper import FormHelper


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['licence_plate', 'color', 'year', 'model', 'transmission']
        widgets = {
            'model': autocomplete.ModelSelect2(url='main:model-autocomplete')
        }


LaborFormSet = inlineformset_factory(WorkOrder, Labor, fields=('__all__'), extra=1)


class WorkOrderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkOrderUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

    class Meta:
        model = WorkOrder
        fields = '__all__'

    labor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))


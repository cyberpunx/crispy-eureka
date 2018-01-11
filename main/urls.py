from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    # /main/
    url(r'^$', views.index_view, name='index'),

    # /main/clients/
    url(r'^clients/$', views.ClientIndexView.as_view(), name='client-index'),

    # /main/clients/<client_id>/
    url(r'^clients/(?P<pk>[0-9]+)/$', views.ClientDetailView.as_view(), name='client-detail'),

    # /main/client/add/
    url(r'clients/add/$', views.ClientCreateView.as_view(), name='client-add'),

    # /main/client/update/<client_id>/
    url(r'clients/update/(?P<pk>[0-9]+)/$', views.ClientUpdateView.as_view(), name='client-update'),

    # /main/client/<client_id>/delete/
    url(r'clients/(?P<pk>[0-9]+)/delete/$', views.ClientDeleteView.as_view(), name='client-delete'),

    # main/vehicles/
    url(r'^vehicles/$', views.VehicleIndexView.as_view(), name='vehicle-index'),

    # main/vehicles/add/
    url(r'vehicles/add/$', views.VehicleCreateView.as_view(), name='vehicle-add'),

    # main/vehicles/add/<client_id>/
    url(r'vehicles/add/(?P<pk>[0-9]+)/$', views.VehicleCreateView.as_view(), name='vehicle-add'),

    # /main/vehicle/update/<vehicle_id>/
    url(r'vehicles/update/(?P<pk>[0-9]+)/$', views.VehicleUpdateView.as_view(), name='vehicle-update'),

    # /main/vehicle/<vehicle_id>/delete/
    url(r'vehicles/(?P<pk>[0-9]+)/delete/$', views.VehicleDeleteView.as_view(), name='vehicle-delete'),

    # main/brands/
    url(r'^brands/$', views.BrandIndexView.as_view(), name='brand-index'),

    # main/brands/add/
    url(r'brands/add/$', views.BrandCreateView.as_view(), name='brand-add'),

    # main/models/
    url(r'^models/$', views.ModelIndexView.as_view(), name='model-index'),

    # main/models/add/
    url(r'models/add/$', views.ModelCreateView.as_view(), name='model-add'),

    # main/category/
    url(r'^category/$', views.CategoryIndexView.as_view(), name='category-index'),

    # main/category/add/
    url(r'category/add/$', views.CategoryCreateView.as_view(), name='category-add'),

    # main/subcat/
    url(r'^subcat/$', views.SubCategoryIndexView.as_view(), name='subcategory-index'),

    # main/subcat/add/
    url(r'subcat/add/$', views.SubCategoryCreateView.as_view(), name='subcategory-add'),

    # /main/employees/
    url(r'^employees/$', views.EmployeeIndexView.as_view(), name='employee-index'),

    # /main/employees/<employee_id>/
    url(r'^employees/(?P<pk>[0-9]+)/$', views.EmployeeDetailView.as_view(), name='employee-detail'),

    # /main/employees/add/
    url(r'employees/add/$', views.EmployeeCreateView.as_view(), name='employee-add'),

    # /main/employees/update/<employee_id>/
    url(r'employees/update/(?P<pk>[0-9]+)/$', views.EmployeeUpdateView.as_view(), name='employee-update'),

    # /main/employees/<employee_id>/delete/
    url(r'employees/(?P<pk>[0-9]+)/delete/$', views.EmployeeDeleteView.as_view(), name='employee-delete'),

    # /main/workorders/
    url(r'workorders/$', views.WorkOrderIndexView.as_view(), name='workorder-index'),

    # /main/workorders/add/
    url(r'workorders/add/$', views.WorkOrderCreateView.as_view(), name='workorder-add'),

    # /main/workorders/<workorder_id>/
    url(r'workorders/(?P<pk>[0-9]+)/$', views.WorkOrderDetailView.as_view(), name='workorder-detail'),

    # /main/workorders/<workorder_id>/
    url(r'workorders/print/(?P<pk>[0-9]+)/$', views.WorkOrderPrintView.as_view(), name='workorder-print'),

    # /main/workorders/<part_id>/delete/
    url(r'workorders/(?P<pk>[0-9]+)/delete/$', views.WorkOrderDeleteView.as_view(), name='workorder-delete'),

    # /main/workorders/update/<workorder_id>/
    url(r'workorders/update/(?P<pk>[0-9]+)/$', views.WorkOrderUpdateView.as_view(), name='workorder-update'),

    # /main/parts/add/<workorder_id>/
    url(r'parts/add/(?P<pk>[0-9]+)/$', views.PartCreateView.as_view(), name='part-add'),

    # /main/parts/update/<employee_id>/
    url(r'parts/update/(?P<pk>[0-9]+)/$', views.PartUpdateView.as_view(), name='part-update'),

    # /main/parts/<part_id>/delete/
    url(r'parts/(?P<pk>[0-9]+)/delete/$', views.PartDeleteView.as_view(), name='part-delete'),

    # /main/works/add/<workorder_id>/
    # url(r'works/add/(?P<pk>[0-9]+)/$', views.WorkCreateView.as_view(), name='work-add'),

    # /main/works/add/<workorder_id>/
    url(r'works/add/(?P<pk>[0-9]+)/$', views.WorkCreateView.as_view(), name='work-add'),

    # /main/works/update/<employee_id>/
    url(r'works/update/(?P<pk>[0-9]+)/$', views.WorkUpdateView.as_view(), name='work-update'),

    # /main/works/<part_id>/delete/
    url(r'works/(?P<pk>[0-9]+)/delete/$', views.WorkDeleteView.as_view(), name='work-delete'),

    # autocomplete
    url(r'^model-autocomplete/$', views.ModelAutocomplete.as_view(), name='model-autocomplete'),
    url(r'^vehicle-autocomplete/$', views.VehicleAutocomplete.as_view(), name='vehicle-autocomplete'),
    url(r'^client-autocomplete/$', views.ClientAutocomplete.as_view(), name='client-autocomplete'),
    url(r'^subcategory-autocomplete/$', views.SubcategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
]
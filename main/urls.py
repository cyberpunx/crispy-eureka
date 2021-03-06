from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views



app_name = 'main'
urlpatterns = [
    # /main/
    url(r'^$', views.index_view, name='index'),

    # /main/welcome
    url(r'^welcome/$', views.welcome_view, name='welcome'),

    # /main/login/
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),

    # /main/profile/
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    # /main/timer/add/<workorder_id>/
    url(r'^timer/add/(?P<pk>[0-9]+)/$', views.timer_create_view, name='timer-add'),

    # /main/timer/stop/<timer_id>/
    url(r'^timer/stop/(?P<pk>[0-9]+)/$', views.timer_stop_view, name='timer-stop'),

    # /main/logout/
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

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

    # /main/client/<client_id>/history/
    url(r'clients/(?P<pk>[0-9]+)/history/$', views.ClientHistoryView.as_view(), name='client-history'),

    # main/vehicles/
    url(r'^vehicles/$', views.VehicleIndexView.as_view(), name='vehicle-index'),

    # main/vehicles/add/
    url(r'vehicles/add/$', views.VehicleClientCreateView.as_view(), name='vehicleclient-add'),

    # main/vehicles/add/<client_id>/
    url(r'vehicles/add/(?P<pk>[0-9]+)/$', views.VehicleCreateView.as_view(), name='vehicle-add'),

    # /main/vehicle/update/<vehicle_id>/
    url(r'vehicles/update/(?P<pk>[0-9]+)/$', views.VehicleUpdateView.as_view(), name='vehicle-update'),

    # /main/vehicle/<vehicle_id>/delete/
    url(r'vehicles/(?P<pk>[0-9]+)/delete/$', views.VehicleDeleteView.as_view(), name='vehicle-delete'),

    # /main/vehicle/<vehicle_id>/history/
    url(r'vehicles/(?P<pk>[0-9]+)/history/$', views.VehicleHistoryView.as_view(), name='vehicle-history'),

    # main/brands/
    url(r'^brands/$', views.BrandIndexView.as_view(), name='brand-index'),

    # main/brands/add/
    url(r'brands/add/$', views.BrandCreateView.as_view(), name='brand-add'),

    # main/models/
    url(r'^models/$', views.ModelIndexView.as_view(), name='model-index'),

    # main/models/add/
    url(r'models/add/$', views.ModelCreateView.as_view(), name='model-add'),

    # main/workcategory/
    url(r'^workcategory/$', views.WorkCategoryIndexView.as_view(), name='workcategory-index'),

    # main/workcategory/add/
    url(r'workcategory/add/$', views.WorkCategoryCreateView.as_view(), name='workcategory-add'),

    # /main/workcategory/<workcategory_id>/delete/
    url(r'workcategory/(?P<pk>[0-9]+)/delete/$', views.WorkCategoryDeleteView.as_view(), name='workcategory-delete'),

    # main/partcategory/
    url(r'^partcategory/$', views.PartCategoryIndexView.as_view(), name='partcategory-index'),

    # main/partcategory/add/
    url(r'partcategory/add/$', views.PartCategoryCreateView.as_view(), name='partcategory-add'),

    # /main/partcategory/<partcategory_id>/delete/
    url(r'partcategory/(?P<pk>[0-9]+)/delete/$', views.PartCategoryDeleteView.as_view(), name='partcategory-delete'),

    # /main/employee/
    url(r'^employee/$', views.EmployeeIndexView.as_view(), name='employee-index'),

    # /main/employee/<employee_id>/
    url(r'^employee/(?P<pk>[0-9]+)/$', views.EmployeeDetailView.as_view(), name='employee-detail'),

    # /main/employee/add/
    url(r'employee/add/$', views.EmployeeCreateView.as_view(), name='employee-add'),

    # /main/employee/update/<employee_id>/
    url(r'employee/update/(?P<pk>[0-9]+)/$', views.EmployeeUpdateView.as_view(), name='employee-update'),

    # /main/employee/<employee_id>/delete/
    url(r'employee/(?P<pk>[0-9]+)/delete/$', views.EmployeeDeleteView.as_view(), name='employee-delete'),

    # /main/workorders/
    url(r'workorders/$', views.WorkOrderIndexView.as_view(), name='workorder-index'),

    # /main/workorders/add/
    url(r'workorders/add/$', views.WorkOrderCreateView.as_view(), name='workorder-add'),

    # /main/workorders/<workorder_id>/
    url(r'workorders/(?P<pk>[0-9]+)/$', views.WorkOrderDetailView.as_view(), name='workorder-detail'),

    # /main/workorders-user/<workorder_id>/
    url(r'workorders-user/(?P<pk>[0-9]+)/$', views.WorkOrderUserDetailView.as_view(), name='workorder-user-detail'),

    # /main/workorders/<workorder_id>/
    url(r'workorders/print/(?P<pk>[0-9]+)/$', views.WorkOrderPrintView.as_view(), name='workorder-print'),

    url(r'workorders/signature_in/(?P<pk>[0-9]+)/$', views.WorkOrderSingatureInView.as_view(), name='workorder-signature-in'),
    url(r'workorders/signature_out/(?P<pk>[0-9]+)/$', views.WorkOrderSingatureOutView.as_view(), name='workorder-signature-out'),

    # /main/workorders/<part_id>/delete/
    url(r'workorders/(?P<pk>[0-9]+)/delete/$', views.WorkOrderDeleteView.as_view(), name='workorder-delete'),

    # /main/workorders/update/<workorder_id>/
    url(r'workorders/update/(?P<pk>[0-9]+)/$', views.WorkOrderUpdateView.as_view(), name='workorder-update'),

    # /main/workorders/updatedetails/<workorder_id>/
    url(r'workorders/updatedetails/(?P<pk>[0-9]+)/$', views.WorkOrderUpdateDetailsView.as_view(), name='workorder-update-details'),

    # /main/parts/
    url(r'parts/$', views.PartIndexView.as_view(), name='part-index'),

    # /main/parts/add/
    url(r'parts/add/$', views.PartCreateView.as_view(), name='part-add'),

    # /main/parts/update/<part_id>/
    url(r'parts/update/(?P<pk>[0-9]+)/$', views.PartUpdateView.as_view(), name='part-update'),

    # /main/parts/<part_id>/delete/
    url(r'parts/(?P<pk>[0-9]+)/delete/$', views.PartDeleteView.as_view(), name='part-delete'),

    # /main/works/
    url(r'works/$', views.WorkIndexView.as_view(), name='work-index'),

    # /main/works/add/
    url(r'works/add/$', views.WorkCreateView.as_view(), name='work-add'),

    # /main/works/update/<work_id>/
    url(r'works/update/(?P<pk>[0-9]+)/$', views.WorkUpdateView.as_view(), name='work-update'),

    # /main/works/<work_id>/delete/
    url(r'works/(?P<pk>[0-9]+)/delete/$', views.WorkDeleteView.as_view(), name='work-delete'),

    # /main/workorderparts/add/<workorder_id>/
    url(r'parts/workorderparts/(?P<pk>[0-9]+)/$', views.WorkOrderPartsCreateView.as_view(), name='workorderparts-add'),

    # /main/workorderparts/<workorder_id>/delete
    url(r'parts/workorderparts/(?P<pk>[0-9]+)/delete$', views.WorkOrderPartsDeleteView.as_view(), name='workorderparts-delete'),

    # /main/workorderparts/<workorder_id>/listdelete
    url(r'parts/workorderparts/(?P<pk>[0-9]+)/listdelete$', views.WorkOrderPartsListDeleteView.as_view(), name='workorderparts-listdelete'),

    # /main/workorderworks/add/<workorder_id>/
    url(r'parts/workorderworks/(?P<pk>[0-9]+)/$', views.WorkOrderWorksCreateView.as_view(), name='workorderworks-add'),

    # /main/workorderworks/<workorder_id>/delete
    url(r'parts/workorderworks/(?P<pk>[0-9]+)/delete$', views.WorkOrderWorksDeleteView.as_view(), name='workorderworks-delete'),

    # /main/workorderworks/<workorder_id>/listdelete
    url(r'parts/workorderworks/(?P<pk>[0-9]+)/listdelete$', views.WorkOrderWorksListDeleteView.as_view(), name='workorderworks-listdelete'),

    # /main/movements/add/<workorder_id>/
    url(r'parts/movements/(?P<pk>[0-9]+)/$', views.MovementCreateView.as_view(), name='movements-add'),

    # autocomplete
    url(r'^model-autocomplete/$', views.ModelAutocomplete.as_view(), name='model-autocomplete'),
    url(r'^vehicle-autocomplete/$', views.VehicleAutocomplete.as_view(), name='vehicle-autocomplete'),
    url(r'^client-autocomplete/$', views.ClientAutocomplete.as_view(), name='client-autocomplete'),
    url(r'^workcategory-autocomplete/$', views.WorkCategoryAutocomplete.as_view(), name='workcategory-autocomplete'),
    url(r'^partcategory-autocomplete/$', views.PartCategoryAutocomplete.as_view(), name='partcategory-autocomplete'),
    url(r'^works-autocomplete/$', views.WorksAutocomplete.as_view(), name='works-autocomplete'),
    url(r'^parts-autocomplete/$', views.PartsAutocomplete.as_view(), name='parts-autocomplete'),


    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),


]
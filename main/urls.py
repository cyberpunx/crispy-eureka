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
]
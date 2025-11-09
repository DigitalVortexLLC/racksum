from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'sites', views.SiteViewSet, basename='site')
router.register(r'devices', views.DeviceViewSet, basename='device')
router.register(r'racks', views.RackViewSet, basename='rack')

urlpatterns = [
    # Custom endpoints (order matters - specific before general)
    path('load', views.load_rack_config, name='load-config'),
    path('devices-json', views.get_devices, name='devices-json'),

    # Rack configuration endpoints (specific before general)
    path('sites/<int:site_id>/racks/<str:rack_name>', views.get_rack_configuration, name='get-rack-config'),
    path('sites/<int:site_id>/racks', views.rack_operations_view, name='rack-operations'),
    path('rack-configs/<int:rack_id>', views.delete_rack_configuration, name='delete-rack-config'),
    path('rack-configs', views.get_all_racks, name='get-all-racks'),

    # Device and Rack management endpoints
    path('sites/<int:site_id>/create-rack', views.create_rack, name='create-rack'),
    path('racks/<int:rack_id>/add-device', views.add_device_to_rack, name='add-device-to-rack'),
    path('rack-devices/<int:rack_device_id>', views.remove_device_from_rack, name='remove-device-from-rack'),

    # Resource usage endpoints
    path('sites/<int:site_id>/resource-usage', views.get_site_resource_usage, name='site-resource-usage'),
    path('racks/<int:rack_id>/resource-usage', views.get_rack_resource_usage, name='rack-resource-usage'),

    # Include router URLs (sites, devices, racks CRUD)
    path('', include(router.urls)),
]

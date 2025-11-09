from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'sites', views.SiteViewSet, basename='site')

urlpatterns = [
    # Custom endpoints (order matters - specific before general)
    path('load', views.load_rack_config, name='load-config'),
    path('devices', views.get_devices, name='devices'),

    # Rack configuration endpoints (specific before general)
    path('sites/<int:site_id>/racks/<str:rack_name>', views.get_rack_configuration, name='get-rack-config'),
    path('sites/<int:site_id>/racks', views.rack_operations_view, name='rack-operations'),
    path('racks/<int:rack_id>', views.delete_rack_configuration, name='delete-rack'),
    path('racks', views.get_all_racks, name='get-all-racks'),

    # Include router URLs (sites CRUD)
    path('', include(router.urls)),
]

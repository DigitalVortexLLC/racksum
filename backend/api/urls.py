from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import passkey_views

# Create router for ViewSets (trailing_slash=False allows URLs without trailing slashes)
router = DefaultRouter(trailing_slash=False)
router.register(r"sites", views.SiteViewSet, basename="site")
router.register(r"devices", views.DeviceViewSet, basename="device")
router.register(r"racks", views.RackViewSet, basename="rack")
router.register(r"providers", views.ProviderViewSet, basename="provider")

urlpatterns = [
    # Custom endpoints (order matters - specific before general)
    path("load", views.load_rack_config, name="load-config"),
    path("devices-json", views.get_devices, name="devices-json"),
    path("validation-schemas", views.get_validation_schemas, name="validation-schemas"),
    # Rack configuration endpoints (specific before general)
    path("sites/<int:site_id>/racks/<str:rack_name>", views.get_rack_configuration, name="get-rack-config"),
    path("sites/<int:site_id>/racks", views.rack_operations_view, name="rack-operations"),
    path("rack-configs/<int:rack_id>", views.delete_rack_configuration, name="delete-rack-config"),
    path("rack-configs", views.get_all_racks, name="get-all-racks"),
    # Device and Rack management endpoints
    path("sites/<int:site_id>/create-rack", views.create_rack, name="create-rack"),
    path("racks/<int:rack_id>/add-device", views.add_device_to_rack, name="add-device-to-rack"),
    path("rack-devices/<int:rack_device_id>", views.remove_device_from_rack, name="remove-device-from-rack"),
    # Provider management endpoints
    path("sites/<int:site_id>/create-provider", views.create_provider, name="create-provider"),
    # Resource usage endpoints
    path("sites/<int:site_id>/resource-usage", views.get_site_resource_usage, name="site-resource-usage"),
    path("racks/<int:rack_id>/resource-usage", views.get_rack_resource_usage, name="rack-resource-usage"),
    # Passkey/WebAuthn authentication endpoints
    path("auth/config", passkey_views.auth_config, name="auth-config"),
    path("auth/passkey/register/begin", passkey_views.begin_registration, name="passkey-register-begin"),
    path("auth/passkey/register/complete", passkey_views.complete_registration, name="passkey-register-complete"),
    path("auth/passkey/login/begin", passkey_views.begin_authentication, name="passkey-login-begin"),
    path("auth/passkey/login/complete", passkey_views.complete_authentication, name="passkey-login-complete"),
    path("auth/passkey/list", passkey_views.list_passkeys, name="passkey-list"),
    path("auth/passkey/<int:passkey_id>", passkey_views.delete_passkey, name="passkey-delete"),
    path("auth/logout", passkey_views.logout_view, name="logout"),
    path("auth/user", passkey_views.current_user, name="current-user"),
    # Include router URLs (sites, devices, racks CRUD)
    path("", include(router.urls)),
]

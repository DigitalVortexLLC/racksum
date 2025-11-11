from django.contrib import admin
from .models import Site, RackConfiguration, Device, Rack, RackDevice, Passkey, PasskeyChallenge


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    """
    Admin interface for Site model
    """

    list_display = ["id", "name", "description", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["name"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for Device model
    """

    list_display = ["id", "device_id", "name", "category", "ru_size", "power_draw", "color", "created_at"]
    list_filter = ["category", "created_at", "updated_at"]
    search_fields = ["device_id", "name", "category", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["category", "name"]

    fieldsets = (
        ("Basic Information", {"fields": ("device_id", "name", "category", "description")}),
        ("Physical Specifications", {"fields": ("ru_size", "power_draw", "color")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    """
    Admin interface for Rack model
    """

    list_display = ["id", "name", "site", "ru_height", "device_count", "power_usage", "created_at"]
    list_filter = ["site", "created_at", "updated_at"]
    search_fields = ["name", "site__name", "description"]
    readonly_fields = ["created_at", "updated_at", "power_usage", "hvac_usage"]
    ordering = ["site", "name"]
    raw_id_fields = ["site"]

    fieldsets = (
        ("Basic Information", {"fields": ("site", "name", "ru_height", "description")}),
        ("Resource Usage", {"fields": ("power_usage", "hvac_usage"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def device_count(self, obj):
        """Display number of devices in rack"""
        return obj.rack_devices.count()

    device_count.short_description = "Devices"

    def power_usage(self, obj):
        """Display total power usage"""
        return f"{obj.get_power_utilization()} W"

    power_usage.short_description = "Power Draw"

    def hvac_usage(self, obj):
        """Display HVAC load"""
        return f"{obj.get_hvac_load():.2f} BTU/hr"

    hvac_usage.short_description = "HVAC Load"


@admin.register(RackDevice)
class RackDeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for RackDevice model
    """

    list_display = ["id", "rack", "device", "position", "instance_name", "power_draw", "created_at"]
    list_filter = ["rack__site", "rack", "device__category", "created_at"]
    search_fields = ["rack__name", "device__name", "instance_name"]
    readonly_fields = ["created_at", "updated_at", "power_draw", "hvac_load"]
    ordering = ["rack", "position"]
    raw_id_fields = ["rack", "device"]

    fieldsets = (
        ("Placement", {"fields": ("rack", "device", "position", "instance_name")}),
        ("Resource Usage", {"fields": ("power_draw", "hvac_load"), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def power_draw(self, obj):
        """Display device power draw"""
        return f"{obj.device.power_draw} W"

    power_draw.short_description = "Power Draw"

    def hvac_load(self, obj):
        """Display device HVAC load"""
        return f"{obj.device.power_draw * 3.41:.2f} BTU/hr"

    hvac_load.short_description = "HVAC Load"


@admin.register(RackConfiguration)
class RackConfigurationAdmin(admin.ModelAdmin):
    """
    Admin interface for RackConfiguration model
    """

    list_display = ["id", "name", "site", "created_at", "updated_at"]
    list_filter = ["site", "created_at", "updated_at"]
    search_fields = ["name", "site__name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["site", "name"]
    raw_id_fields = ["site"]

    fieldsets = (
        ("Basic Information", {"fields": ("site", "name", "description")}),
        ("Configuration Data", {"fields": ("config_data",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Passkey)
class PasskeyAdmin(admin.ModelAdmin):
    """
    Admin interface for Passkey model
    """

    list_display = ["id", "user", "name", "created_at", "last_used_at"]
    list_filter = ["created_at", "last_used_at"]
    search_fields = ["user__username", "name", "aaguid"]
    readonly_fields = ["credential_id", "public_key", "sign_count", "aaguid", "created_at", "last_used_at"]
    ordering = ["-created_at"]
    raw_id_fields = ["user"]

    fieldsets = (
        ("User Information", {"fields": ("user", "name")}),
        ("Credential Data", {"fields": ("credential_id", "public_key", "sign_count", "transports", "aaguid")}),
        ("Usage", {"fields": ("created_at", "last_used_at")}),
    )


@admin.register(PasskeyChallenge)
class PasskeyChallengeAdmin(admin.ModelAdmin):
    """
    Admin interface for PasskeyChallenge model
    """

    list_display = ["id", "user", "challenge_type", "created_at", "expires_at", "is_expired"]
    list_filter = ["challenge_type", "created_at"]
    search_fields = ["user__username"]
    readonly_fields = ["challenge", "created_at"]
    ordering = ["-created_at"]
    raw_id_fields = ["user"]

    def is_expired(self, obj):
        """Check if challenge is expired"""
        from django.utils import timezone

        return obj.expires_at < timezone.now()

    is_expired.boolean = True
    is_expired.short_description = "Expired"

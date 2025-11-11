from rest_framework import serializers
from django.db import models
from .models import Site, RackConfiguration, Device, Rack, RackDevice, Provider
from .validation_schemas import (
    validate_hex_color,
    validate_non_empty_string,
    validate_provider_placement,
    validate_ru_size,
    validate_power_draw
)


class SiteSerializer(serializers.ModelSerializer):
    """
    Serializer for Site model
    """
    class Meta:
        model = Site
        fields = ['id', 'uuid', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at']


class RackConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for RackConfiguration model
    """
    site_id = serializers.IntegerField(source='site.id', read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)

    class Meta:
        model = RackConfiguration
        fields = [
            'id',
            'site_id',
            'site_name',
            'name',
            'description',
            'config_data',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'site_id', 'site_name', 'created_at', 'updated_at']


class RackConfigurationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating RackConfiguration
    """
    class Meta:
        model = RackConfiguration
        fields = ['id', 'name', 'description', 'config_data']
        read_only_fields = ['id']

    def validate_name(self, value):
        """
        Validate that name is not empty
        """
        return validate_non_empty_string(value, "Rack name")

    def validate_config_data(self, value):
        """
        Validate that config_data is a valid object
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Configuration data must be a valid object")
        return value


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for Device model
    """
    class Meta:
        model = Device
        fields = [
            'id',
            'device_id',
            'name',
            'category',
            'ru_size',
            'power_draw',
            'power_ports_used',
            'color',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_device_id(self, value):
        """Validate device_id is not empty"""
        return validate_non_empty_string(value, "Device ID")

    def validate_color(self, value):
        """Validate color is a valid hex code"""
        return validate_hex_color(value)


class RackDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for RackDevice with nested device information
    """
    device_info = DeviceSerializer(source='device', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = RackDevice
        fields = [
            'id',
            'rack',
            'device',
            'device_info',
            'device_name',
            'position',
            'instance_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RackDeviceCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating RackDevice instances
    """
    class Meta:
        model = RackDevice
        fields = ['id', 'device', 'position', 'instance_name']
        read_only_fields = ['id']

    def validate(self, data):
        """Validate that the device fits at the specified position"""
        device = data.get('device')
        position = data.get('position')
        rack = self.context.get('rack')

        if rack and device:
            # Check if device fits within rack height
            if position + device.ru_size - 1 > rack.ru_height:
                raise serializers.ValidationError(
                    f"Device does not fit at position {position}. "
                    f"Requires {device.ru_size} RU but only {rack.ru_height - position + 1} available."
                )

            # Check for conflicts with existing devices
            for ru in range(position, position + device.ru_size):
                conflict = RackDevice.objects.filter(
                    rack=rack,
                    position__lte=ru,
                    position__gt=ru - models.F('device__ru_size')
                ).exclude(id=self.instance.id if self.instance else None).exists()

                if conflict:
                    raise serializers.ValidationError(
                        f"Position conflict: RU {ru} is already occupied"
                    )

        return data


class RackSerializer(serializers.ModelSerializer):
    """
    Serializer for Rack with nested devices
    """
    devices = RackDeviceSerializer(source='rack_devices', many=True, read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    power_utilization = serializers.SerializerMethodField()
    hvac_load = serializers.SerializerMethodField()
    power_ports_used = serializers.SerializerMethodField()

    class Meta:
        model = Rack
        fields = [
            'id',
            'site',
            'site_name',
            'name',
            'ru_height',
            'description',
            'devices',
            'power_utilization',
            'hvac_load',
            'power_ports_used',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'site_name', 'created_at', 'updated_at']

    def get_power_utilization(self, obj):
        """Get total power draw in watts"""
        return obj.get_power_utilization()

    def get_hvac_load(self, obj):
        """Get heat load in BTU/hr"""
        return obj.get_hvac_load()

    def get_power_ports_used(self, obj):
        """Get total number of PDU power ports used"""
        return obj.get_power_ports_used()


class RackCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Rack instances
    """
    class Meta:
        model = Rack
        fields = ['id', 'name', 'ru_height', 'description']
        read_only_fields = ['id']

    def validate_name(self, value):
        """Validate rack name is not empty"""
        return validate_non_empty_string(value, "Rack name")


class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer for Provider model
    """
    site_name = serializers.CharField(source='site.name', read_only=True)
    rack_name = serializers.CharField(source='rack.name', read_only=True, allow_null=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Provider
        fields = [
            'id',
            'site',
            'site_name',
            'name',
            'type',
            'type_display',
            'description',
            'location',
            'power_capacity',
            'power_ports_capacity',
            'cooling_capacity',
            'network_capacity',
            'ru_size',
            'rack',
            'rack_name',
            'position',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'site_name', 'rack_name', 'type_display', 'created_at', 'updated_at']


class ProviderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating Provider instances
    """
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'type',
            'description',
            'location',
            'power_capacity',
            'power_ports_capacity',
            'cooling_capacity',
            'network_capacity',
            'ru_size',
            'rack',
            'position'
        ]
        read_only_fields = ['id']

    def validate_name(self, value):
        """Validate provider name is not empty"""
        return validate_non_empty_string(value, "Provider name")

    def validate(self, data):
        """Validate provider placement rules"""
        ru_size = data.get('ru_size', 0)
        rack = data.get('rack')
        position = data.get('position')

        # Use centralized validation
        validate_provider_placement(
            ru_size=ru_size,
            rack=rack,
            position=position,
            rack_obj=rack,
            provider_instance=self.instance
        )

        return data

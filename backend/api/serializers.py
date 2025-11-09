from rest_framework import serializers
from .models import Site, RackConfiguration


class SiteSerializer(serializers.ModelSerializer):
    """
    Serializer for Site model
    """
    class Meta:
        model = Site
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


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
        if not value or not value.strip():
            raise serializers.ValidationError("Rack name is required")
        return value.strip()

    def validate_config_data(self, value):
        """
        Validate that config_data is a valid object
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Configuration data must be a valid object")
        return value

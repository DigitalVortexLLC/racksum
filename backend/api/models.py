from django.db import models
from django.core.validators import MinValueValidator


class Device(models.Model):
    """
    Represents a device type/template that can be placed in racks
    """
    device_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True)
    ru_size = models.IntegerField(validators=[MinValueValidator(0)])
    power_draw = models.IntegerField(validators=[MinValueValidator(0)], help_text="Power consumption in watts")
    color = models.CharField(max_length=7, default="#000000", help_text="Hex color code for display")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class Site(models.Model):
    """
    Represents a physical location/datacenter
    """
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sites'
        ordering = ['name']

    def __str__(self):
        return self.name


class RackConfiguration(models.Model):
    """
    Stores complete rack layouts for a site
    """
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='rack_configurations',
        db_column='site_id'
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    config_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rack_configurations'
        unique_together = [['site', 'name']]
        ordering = ['name']
        indexes = [
            models.Index(fields=['site']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.site.name} - {self.name}"


class Rack(models.Model):
    """
    Represents an individual rack within a site
    """
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='racks',
        db_column='site_id'
    )
    name = models.CharField(max_length=255)
    ru_height = models.IntegerField(default=42, validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'racks'
        unique_together = [['site', 'name']]
        ordering = ['site', 'name']
        indexes = [
            models.Index(fields=['site']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.site.name} - {self.name}"

    def get_power_utilization(self):
        """Calculate total power draw from all devices in this rack"""
        total_power = 0
        for rack_device in self.rack_devices.all():
            total_power += rack_device.device.power_draw
        return total_power

    def get_hvac_load(self):
        """Calculate heat load in BTU/hr (1W = 3.41 BTU/hr)"""
        return self.get_power_utilization() * 3.41


class RackDevice(models.Model):
    """
    Represents a device instance placed in a specific rack at a specific position
    """
    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name='rack_devices',
        db_column='rack_id'
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='rack_placements',
        db_column='device_id'
    )
    position = models.IntegerField(validators=[MinValueValidator(1)], help_text="Starting RU position (1-based)")
    instance_name = models.CharField(max_length=255, blank=True, null=True, help_text="Custom name for this device instance")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rack_devices'
        unique_together = [['rack', 'position']]
        ordering = ['rack', 'position']
        indexes = [
            models.Index(fields=['rack']),
            models.Index(fields=['device']),
            models.Index(fields=['position']),
        ]

    def __str__(self):
        name = self.instance_name or self.device.name
        return f"{self.rack.name} - {name} @ RU{self.position}"

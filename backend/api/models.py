from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class HardwareProvider(models.Model):
    """
    Represents a hardware/equipment provider
    """

    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hardware_providers"
        ordering = ["name"]

    def __str__(self):
        return self.name


class DeviceGroup(models.Model):
    """
    Represents a logical grouping of device types
    """

    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_groups"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Represents a device type/template that can be placed in racks
    """

    device_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True)
    provider = models.ForeignKey(
        HardwareProvider,
        on_delete=models.SET_NULL,
        related_name="devices",
        db_column="provider_id",
        null=True,
        blank=True,
    )
    device_group = models.ForeignKey(
        DeviceGroup,
        on_delete=models.SET_NULL,
        related_name="devices",
        db_column="device_group_id",
        null=True,
        blank=True,
    )
    ru_size = models.IntegerField(validators=[MinValueValidator(0)])
    power_draw = models.IntegerField(validators=[MinValueValidator(0)], help_text="Power consumption in watts")
    power_ports_used = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=1,
        help_text="Number of PDU power ports required (e.g., 2 for dual PSU)",
    )
    color = models.CharField(max_length=7, default="#000000", help_text="Hex color code for display")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "devices"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["device_id"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class Site(models.Model):
    """
    Represents a physical location/datacenter
    """

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sites"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RackConfiguration(models.Model):
    """
    Stores complete rack layouts for a site
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="rack_configurations", db_column="site_id")
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    config_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rack_configurations"
        unique_together = [["site", "name"]]
        ordering = ["name"]
        indexes = [
            models.Index(fields=["site"]),
            models.Index(fields=["name"]),
            # Composite index for common (site_id, name) lookups
            models.Index(fields=["site", "name"], name="rack_config_site_name_idx"),
        ]

    def __str__(self):
        return f"{self.site.name} - {self.name}"


class Rack(models.Model):
    """
    Represents an individual rack within a site
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="racks", db_column="site_id")
    name = models.CharField(max_length=255)
    ru_height = models.IntegerField(default=42, validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "racks"
        unique_together = [["site", "name"]]
        ordering = ["site", "name"]
        indexes = [
            models.Index(fields=["site"]),
            models.Index(fields=["name"]),
            # Composite index for common (site_id, name) lookups
            models.Index(fields=["site", "name"], name="rack_site_name_idx"),
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

    def get_power_ports_used(self):
        """Calculate total number of PDU power ports used in this rack"""
        total_ports = 0
        for rack_device in self.rack_devices.all():
            total_ports += rack_device.device.power_ports_used
        return total_ports


class RackDevice(models.Model):
    """
    Represents a device instance placed in a specific rack at a specific position
    """

    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="rack_devices", db_column="rack_id")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="rack_placements", db_column="device_id")
    position = models.IntegerField(validators=[MinValueValidator(1)], help_text="Starting RU position (1-based)")
    instance_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Custom name for this device instance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rack_devices"
        unique_together = [["rack", "position"]]
        ordering = ["rack", "position"]
        indexes = [
            models.Index(fields=["rack"]),
            models.Index(fields=["device"]),
            models.Index(fields=["position"]),
        ]

    def __str__(self):
        name = self.instance_name or self.device.name
        return f"{self.rack.name} - {name} @ RU{self.position}"


class Provider(models.Model):
    """
    Represents a resource provider (power, cooling) that can optionally consume RU space
    """

    PROVIDER_TYPES = [
        ("power", "Power"),
        ("cooling", "Cooling"),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="providers", db_column="site_id")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PROVIDER_TYPES, db_index=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Physical location description")

    # Capacity fields (resource provisioning)
    power_capacity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, help_text="Power capacity in watts"
    )
    power_ports_capacity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, help_text="Number of power ports available (for PDUs)"
    )
    cooling_capacity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, help_text="Cooling capacity in BTU/hr"
    )

    # RU space consumption fields (optional rack placement)
    ru_size = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, help_text="Rack units consumed (0 = not racked)"
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="providers",
        db_column="rack_id",
        help_text="Rack where this provider is installed (null = not racked)",
    )
    position = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        help_text="Starting RU position in rack (null = not racked)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resource_providers"
        ordering = ["site", "type", "name"]
        indexes = [
            models.Index(fields=["site"]),
            models.Index(fields=["type"]),
            models.Index(fields=["rack"]),
            # Composite indexes for common queries
            models.Index(fields=["site", "type"], name="provider_site_type_idx"),
            models.Index(fields=["site", "name"], name="provider_site_name_idx"),
            models.Index(fields=["rack", "position"], name="provider_rack_pos_idx"),
        ]
        constraints = [
            # Check constraint: if ru_size is 0, rack and position must be null
            models.CheckConstraint(
                check=(
                    models.Q(ru_size__gt=0)
                    | (models.Q(ru_size=0) & models.Q(rack__isnull=True) & models.Q(position__isnull=True))
                ),
                name="provider_zero_rusize_not_racked",
            ),
            # Check constraint: if racked, must have both rack and position
            models.CheckConstraint(
                check=(
                    (models.Q(rack__isnull=True) & models.Q(position__isnull=True))
                    | (models.Q(rack__isnull=False) & models.Q(position__isnull=False))
                ),
                name="provider_rack_position_together",
            ),
            # Check constraint: position must be positive if set
            models.CheckConstraint(
                check=models.Q(position__isnull=True) | models.Q(position__gte=1),
                name="provider_position_positive",
            ),
        ]

    def __str__(self):
        rack_info = f" @ {self.rack.name} RU{self.position}" if self.rack and self.position else ""
        return f"{self.site.name} - {self.name} ({self.get_type_display()}){rack_info}"

    def clean(self):
        """Validate provider placement"""
        from django.core.exceptions import ValidationError

        # If ru_size is 0, rack and position must be null
        if self.ru_size == 0:
            if self.rack or self.position:
                raise ValidationError("Providers with ru_size=0 cannot be placed in racks")

        # If racked, must have both rack and position
        if (self.rack and not self.position) or (self.position and not self.rack):
            raise ValidationError("Both rack and position must be set for racked providers")

        # If racked, validate placement doesn't exceed rack height
        if self.rack and self.position:
            if self.position + self.ru_size - 1 > self.rack.ru_height:
                raise ValidationError(
                    f"Provider placement exceeds rack height "
                    f"(position {self.position} + size {self.ru_size} > {self.rack.ru_height})"
                )

    def save(self, *args, **kwargs):
        """
        Override save to ensure validation is always run.
        This ensures that clean() validation is enforced at the model level,
        not just in forms or serializers.
        """
        # Run full model validation before saving
        self.full_clean()
        super().save(*args, **kwargs)


class Passkey(models.Model):
    """
    Stores WebAuthn/FIDO2 passkey credentials for passwordless authentication
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passkeys")
    credential_id = models.CharField(
        max_length=255, unique=True, db_index=True, help_text="Base64-encoded credential ID"
    )
    public_key = models.TextField(help_text="Base64-encoded public key")
    sign_count = models.IntegerField(default=0, help_text="Signature counter for replay protection")
    transports = models.JSONField(default=list, blank=True, help_text="Supported transports (usb, nfc, ble, internal)")
    aaguid = models.CharField(max_length=255, blank=True, help_text="Authenticator AAGUID")
    name = models.CharField(max_length=255, help_text="User-friendly name for this passkey")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "passkeys"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["credential_id"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class PasskeyChallenge(models.Model):
    """
    Temporary storage for WebAuthn challenges during registration/authentication
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passkey_challenges", null=True, blank=True)
    challenge = models.CharField(max_length=255, help_text="Base64-encoded challenge")
    challenge_type = models.CharField(
        max_length=20,
        choices=[
            ("registration", "Registration"),
            ("authentication", "Authentication"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Challenge expiration time")

    class Meta:
        db_table = "passkey_challenges"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["challenge"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.challenge_type} challenge"

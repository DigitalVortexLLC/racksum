"""
Centralized validation schemas for the application.
These schemas serve as the single source of truth for validation rules
and can be exposed via API for frontend validation.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
import re


# ==================== Validation Constants ====================

RU_SIZE_MIN = 0
RU_SIZE_MAX = 52
POWER_DRAW_MIN = 0
COLOR_HEX_PATTERN = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')


# ==================== JSON Schema Definitions ====================

DEVICE_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["device_id", "name", "category", "ru_size", "power_draw", "color"],
    "properties": {
        "device_id": {
            "type": "string",
            "minLength": 1,
            "description": "Unique device identifier"
        },
        "name": {
            "type": "string",
            "minLength": 1,
            "description": "Device name"
        },
        "category": {
            "type": "string",
            "minLength": 1,
            "description": "Device category (server, storage, network, etc.)"
        },
        "ru_size": {
            "type": "number",
            "minimum": RU_SIZE_MIN,
            "maximum": RU_SIZE_MAX,
            "description": "Rack units consumed by device"
        },
        "power_draw": {
            "type": "number",
            "minimum": POWER_DRAW_MIN,
            "description": "Power consumption in watts"
        },
        "power_ports_used": {
            "type": "number",
            "minimum": 1,
            "default": 1,
            "description": "Number of PDU power ports required"
        },
        "color": {
            "type": "string",
            "pattern": "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
            "description": "Hex color code (e.g., #4CAF50)"
        },
        "description": {
            "type": "string",
            "description": "Optional device description"
        }
    }
}

RACK_CONFIG_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["settings", "racks"],
    "properties": {
        "settings": {
            "type": "object",
            "required": ["totalPowerCapacity", "hvacCapacity", "ruPerRack"],
            "properties": {
                "totalPowerCapacity": {
                    "type": "number",
                    "minimum": 0,
                    "description": "Total power capacity in watts"
                },
                "hvacCapacity": {
                    "type": "number",
                    "minimum": 0,
                    "description": "HVAC capacity in BTU/hr"
                },
                "ruPerRack": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": RU_SIZE_MAX,
                    "description": "Rack units per rack"
                }
            }
        },
        "racks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name", "devices"],
                "properties": {
                    "id": {
                        "type": ["string", "number"],
                        "description": "Rack identifier"
                    },
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Rack name"
                    },
                    "devices": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["position", "ruSize"],
                            "properties": {
                                "deviceId": {
                                    "type": ["string", "number"],
                                    "description": "Device identifier"
                                },
                                "id": {
                                    "type": ["string", "number"],
                                    "description": "Alternative device identifier"
                                },
                                "position": {
                                    "type": "number",
                                    "minimum": 1,
                                    "description": "Starting RU position"
                                },
                                "ruSize": {
                                    "type": "number",
                                    "minimum": 1,
                                    "maximum": RU_SIZE_MAX,
                                    "description": "Device size in RU"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

RACK_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "description": "Rack name"
        },
        "ru_height": {
            "type": "number",
            "minimum": 1,
            "maximum": RU_SIZE_MAX,
            "default": 42,
            "description": "Rack height in RU"
        },
        "description": {
            "type": "string",
            "description": "Optional rack description"
        }
    }
}

PROVIDER_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "description": "Provider name"
        },
        "type": {
            "type": "string",
            "enum": ["power", "cooling"],
            "description": "Provider type"
        },
        "description": {
            "type": "string",
            "description": "Optional provider description"
        },
        "location": {
            "type": "string",
            "description": "Physical location description"
        },
        "power_capacity": {
            "type": "number",
            "minimum": 0,
            "default": 0,
            "description": "Power capacity in watts"
        },
        "power_ports_capacity": {
            "type": "number",
            "minimum": 0,
            "default": 0,
            "description": "Number of power ports available"
        },
        "cooling_capacity": {
            "type": "number",
            "minimum": 0,
            "default": 0,
            "description": "Cooling capacity in BTU/hr"
        },
        "ru_size": {
            "type": "number",
            "minimum": 0,
            "maximum": RU_SIZE_MAX,
            "default": 0,
            "description": "Rack units consumed (0 = not racked)"
        },
        "rack": {
            "type": ["number", "null"],
            "description": "Rack ID where provider is installed"
        },
        "position": {
            "type": ["number", "null"],
            "minimum": 1,
            "description": "Starting RU position in rack"
        }
    }
}


# ==================== Validation Helper Functions ====================

def validate_hex_color(value):
    """
    Validate that a string is a valid hex color code.

    Args:
        value: Color string to validate

    Returns:
        Normalized color string (with # prefix)

    Raises:
        serializers.ValidationError: If color is invalid
    """
    if not value:
        raise serializers.ValidationError("Color is required")

    # Ensure # prefix
    if not value.startswith('#'):
        value = '#' + value

    # Validate hex format
    if not COLOR_HEX_PATTERN.match(value):
        raise serializers.ValidationError(
            "Color must be a valid hex code (e.g., #4CAF50 or #FFF)"
        )

    return value


def validate_ru_size(value, min_val=RU_SIZE_MIN, max_val=RU_SIZE_MAX):
    """
    Validate rack unit size.

    Args:
        value: RU size to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Raises:
        serializers.ValidationError: If RU size is invalid
    """
    if not isinstance(value, (int, float)):
        raise serializers.ValidationError("RU size must be a number")

    if value < min_val or value > max_val:
        raise serializers.ValidationError(
            f"RU size must be between {min_val} and {max_val}"
        )


def validate_power_draw(value):
    """
    Validate power draw value.

    Args:
        value: Power draw to validate (in watts)

    Raises:
        serializers.ValidationError: If power draw is invalid
    """
    if not isinstance(value, (int, float)):
        raise serializers.ValidationError("Power draw must be a number")

    if value < POWER_DRAW_MIN:
        raise serializers.ValidationError(
            f"Power draw must be at least {POWER_DRAW_MIN} watts"
        )


def validate_non_empty_string(value, field_name="Field"):
    """
    Validate that a string is not empty after stripping whitespace.

    Args:
        value: String to validate
        field_name: Name of the field for error messages

    Returns:
        Stripped string

    Raises:
        serializers.ValidationError: If string is empty
    """
    if not value or not isinstance(value, str):
        raise serializers.ValidationError(f"{field_name} is required")

    value = value.strip()
    if not value:
        raise serializers.ValidationError(f"{field_name} cannot be empty")

    return value


def validate_provider_placement(ru_size, rack, position, rack_obj=None,
                                provider_instance=None):
    """
    Validate provider placement rules.

    Args:
        ru_size: RU size of the provider
        rack: Rack ID or None
        position: Position in rack or None
        rack_obj: Optional Rack model instance
        provider_instance: Optional Provider instance (for updates)

    Raises:
        serializers.ValidationError: If placement is invalid
    """
    from .models import RackDevice, Provider
    from django.db import models

    # If ru_size is 0, rack and position must be null
    if ru_size == 0:
        if rack or position:
            raise serializers.ValidationError(
                "Providers with ru_size=0 cannot be placed in racks"
            )
        return

    # If racked, must have both rack and position
    if (rack and not position) or (position and not rack):
        raise serializers.ValidationError(
            "Both rack and position must be set for racked providers"
        )

    # If racked, validate placement
    if rack and position and rack_obj:
        # Check if provider exceeds rack height
        if position + ru_size - 1 > rack_obj.ru_height:
            raise serializers.ValidationError(
                f"Provider placement exceeds rack height "
                f"(position {position} + size {ru_size} > {rack_obj.ru_height})"
            )

        # Check for conflicts with existing devices
        for ru in range(position, position + ru_size):
            device_conflict = RackDevice.objects.filter(
                rack=rack_obj,
                position__lte=ru,
                position__gt=ru - models.F('device__ru_size')
            ).exclude(
                id=provider_instance.id if provider_instance else None
            ).exists()

            if device_conflict:
                raise serializers.ValidationError(
                    f"Position conflict with device: RU {ru} is already occupied"
                )

        # Check for conflicts with other providers
        provider_conflict = Provider.objects.filter(
            rack=rack_obj,
            position__lte=position + ru_size - 1,
            position__gte=position - models.F('ru_size') + 1
        ).exclude(
            id=provider_instance.id if provider_instance else None
        ).exists()

        if provider_conflict:
            raise serializers.ValidationError(
                f"Position conflict with another provider at position {position}"
            )


def get_all_schemas():
    """
    Get all validation schemas for API exposure.

    Returns:
        Dictionary of all validation schemas
    """
    return {
        "device": DEVICE_VALIDATION_SCHEMA,
        "rack_config": RACK_CONFIG_VALIDATION_SCHEMA,
        "rack": RACK_VALIDATION_SCHEMA,
        "provider": PROVIDER_VALIDATION_SCHEMA,
        "constants": {
            "RU_SIZE_MIN": RU_SIZE_MIN,
            "RU_SIZE_MAX": RU_SIZE_MAX,
            "POWER_DRAW_MIN": POWER_DRAW_MIN,
        }
    }

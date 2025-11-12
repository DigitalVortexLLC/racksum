"""
JSON formatting functions for MCP server responses
"""

import json
from typing import Dict, List, Any


def format_site_stats_json(sites: List[Any]) -> str:
    """Format site statistics as JSON"""
    if not sites:
        return json.dumps({"sites": [], "message": "No sites found"})

    sites_data = []
    for site in sites:
        racks = list(site.racks.all())
        total_devices = sum(rack.rack_devices.count() for rack in racks)
        total_power = sum(rack.get_power_utilization() for rack in racks)
        total_hvac = sum(rack.get_hvac_load() for rack in racks)

        sites_data.append(
            {
                "name": site.name,
                "description": site.description or "",
                "racks_count": len(racks),
                "devices_count": total_devices,
                "power_watts": round(total_power, 2),
                "power_kw": round(total_power / 1000, 2),
                "hvac_btu_hr": round(total_hvac, 2),
                "hvac_tons": round(total_hvac / 12000, 2),  # Will be replaced with settings
                "created_at": site.created_at.isoformat(),
            }
        )

    return json.dumps({"sites": sites_data}, indent=2)


def format_site_details_json(site: Any) -> str:
    """Format site details as JSON"""
    racks_data = []

    for rack in site.racks.all():
        devices = list(rack.rack_devices.all())
        power = rack.get_power_utilization()
        hvac = rack.get_hvac_load()
        ru_used = sum(device.device.ru_size for device in devices)
        ru_available = rack.ru_height - ru_used

        racks_data.append(
            {
                "name": rack.name,
                "description": rack.description or "",
                "ru_height": rack.ru_height,
                "ru_used": ru_used,
                "ru_available": ru_available,
                "utilization_percent": round((ru_used / rack.ru_height * 100) if rack.ru_height > 0 else 0, 1),
                "devices_count": len(devices),
                "power_watts": round(power, 2),
                "power_kw": round(power / 1000, 2),
                "hvac_btu_hr": round(hvac, 2),
                "hvac_tons": round(hvac / 12000, 2),
            }
        )

    site_data = {
        "name": site.name,
        "description": site.description or "",
        "created_at": site.created_at.isoformat(),
        "updated_at": site.updated_at.isoformat(),
        "racks_count": len(racks_data),
        "racks": racks_data,
    }

    return json.dumps(site_data, indent=2)


def format_rack_details_json(site: Any, rack: Any) -> str:
    """Format rack details as JSON"""
    devices = list(rack.rack_devices.all())
    ru_used = sum(device.device.ru_size for device in devices)
    ru_available = rack.ru_height - ru_used
    power = rack.get_power_utilization()
    hvac = rack.get_hvac_load()

    devices_data = []
    for rack_device in devices:
        device = rack_device.device
        display_name = rack_device.instance_name or device.name

        devices_data.append(
            {
                "instance_name": display_name,
                "device_type": device.name,
                "category": device.category,
                "position": rack_device.position,
                "ru_size": device.ru_size,
                "power_watts": device.power_draw,
                "heat_btu_hr": round(device.power_draw * 3.412, 2),  # Will be replaced with settings
            }
        )

    rack_data = {
        "site_name": site.name,
        "rack_name": rack.name,
        "description": rack.description or "",
        "ru_height": rack.ru_height,
        "ru_used": ru_used,
        "ru_available": ru_available,
        "utilization_percent": round((ru_used / rack.ru_height * 100) if rack.ru_height > 0 else 0, 1),
        "power_watts": round(power, 2),
        "power_kw": round(power / 1000, 2),
        "hvac_btu_hr": round(hvac, 2),
        "hvac_tons": round(hvac / 12000, 2),
        "created_at": rack.created_at.isoformat(),
        "updated_at": rack.updated_at.isoformat(),
        "devices": devices_data,
    }

    return json.dumps(rack_data, indent=2)


def format_available_resources_json(devices_list: List[Any]) -> str:
    """Format available resources as JSON"""
    if not devices_list:
        return json.dumps({"devices": [], "message": "No devices found"})

    # Group by category
    categories_dict = {}
    for device in devices_list:
        if device.category not in categories_dict:
            categories_dict[device.category] = []

        categories_dict[device.category].append(
            {
                "device_id": device.device_id,
                "name": device.name,
                "description": device.description or "",
                "ru_size": device.ru_size,
                "power_watts": device.power_draw,
                "heat_btu_hr": round(device.power_draw * 3.412, 2),
                "color": device.color,
            }
        )

    # Convert to list format
    categories_list = [
        {"category": category, "devices": devices} for category, devices in sorted(categories_dict.items())
    ]

    return json.dumps({"total_device_types": len(devices_list), "categories": categories_list}, indent=2)


def format_resource_summary_json(sites: List[Any], racks: Any, stats: Dict[str, Any]) -> str:
    """Format resource summary as JSON"""
    summary_data = {
        "totals": {
            "sites": stats["total_sites"],
            "racks": stats["total_racks"],
            "devices_installed": stats["total_rack_devices"],
            "device_types_available": stats["total_device_types"],
        },
        "capacity": {
            "ru_total": stats["total_ru_capacity"],
            "ru_used": stats["total_ru_used"],
            "ru_available": stats["total_ru_capacity"] - stats["total_ru_used"],
            "utilization_percent": round(
                (stats["total_ru_used"] / stats["total_ru_capacity"] * 100) if stats["total_ru_capacity"] > 0 else 0, 1
            ),
        },
        "power_cooling": {
            "total_power_watts": round(stats["overall_power"], 2),
            "total_power_kw": round(stats["overall_power"] / 1000, 2),
            "total_hvac_btu_hr": round(stats["overall_hvac"], 2),
            "total_hvac_tons": round(stats["overall_hvac"] / 12000, 2),
            "average_power_per_rack_watts": (
                round(stats["overall_power"] / stats["total_racks"], 2) if stats["total_racks"] > 0 else 0
            ),
            "average_power_per_rack_kw": (
                round(stats["overall_power"] / stats["total_racks"] / 1000, 2) if stats["total_racks"] > 0 else 0
            ),
        },
    }

    return json.dumps(summary_data, indent=2)

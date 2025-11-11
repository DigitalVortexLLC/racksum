"""
Formatting helper functions for MCP server responses
"""

from django.conf import settings


def format_power(watts: float) -> str:
    """Format power consumption in watts and kilowatts"""
    return f"{watts:,.0f} W ({watts/1000:.2f} kW)"


def format_hvac(btu_hr: float) -> str:
    """Format HVAC load in BTU/hr and tons"""
    return f"{btu_hr:,.0f} BTU/hr ({btu_hr/settings.BTU_PER_TON:.2f} tons)"


def format_space_utilization(used: int, total: int) -> str:
    """Format rack space utilization"""
    percentage = (used / total * 100) if total > 0 else 0
    return f"{used}U / {total}U ({percentage:.1f}%)"


def calculate_heat_output(power_watts: float) -> float:
    """Calculate heat output in BTU/hr from power consumption in watts"""
    return power_watts * settings.WATTS_TO_BTU

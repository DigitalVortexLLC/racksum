"""
Tests for MCP server formatters
"""
import pytest
from django.test import TestCase, override_settings
from mcp.formatters import (
    format_power,
    format_hvac,
    format_space_utilization,
    calculate_heat_output
)


class TestFormatters(TestCase):
    """Test cases for formatting helper functions"""

    def test_format_power_basic(self):
        """Test power formatting with basic values"""
        result = format_power(1000)
        self.assertEqual(result, "1,000 W (1.00 kW)")

    def test_format_power_large_value(self):
        """Test power formatting with large values"""
        result = format_power(123456.78)
        self.assertEqual(result, "123,457 W (123.46 kW)")

    def test_format_power_zero(self):
        """Test power formatting with zero"""
        result = format_power(0)
        self.assertEqual(result, "0 W (0.00 kW)")

    def test_format_power_decimal(self):
        """Test power formatting with decimal values"""
        result = format_power(500.5)
        self.assertEqual(result, "500 W (0.50 kW)")

    @override_settings(BTU_PER_TON=12000)
    def test_format_hvac_basic(self):
        """Test HVAC formatting with basic values"""
        result = format_hvac(12000)
        self.assertEqual(result, "12,000 BTU/hr (1.00 tons)")

    @override_settings(BTU_PER_TON=12000)
    def test_format_hvac_fractional_tons(self):
        """Test HVAC formatting with fractional tons"""
        result = format_hvac(18000)
        self.assertEqual(result, "18,000 BTU/hr (1.50 tons)")

    @override_settings(BTU_PER_TON=12000)
    def test_format_hvac_large_value(self):
        """Test HVAC formatting with large values"""
        result = format_hvac(120000)
        self.assertEqual(result, "120,000 BTU/hr (10.00 tons)")

    @override_settings(BTU_PER_TON=12000)
    def test_format_hvac_zero(self):
        """Test HVAC formatting with zero"""
        result = format_hvac(0)
        self.assertEqual(result, "0 BTU/hr (0.00 tons)")

    @override_settings(BTU_PER_TON=10000)
    def test_format_hvac_custom_btu_per_ton(self):
        """Test HVAC formatting with custom BTU_PER_TON setting"""
        result = format_hvac(10000)
        self.assertEqual(result, "10,000 BTU/hr (1.00 tons)")

    def test_format_space_utilization_half(self):
        """Test space utilization at 50%"""
        result = format_space_utilization(21, 42)
        self.assertEqual(result, "21U / 42U (50.0%)")

    def test_format_space_utilization_full(self):
        """Test space utilization at 100%"""
        result = format_space_utilization(42, 42)
        self.assertEqual(result, "42U / 42U (100.0%)")

    def test_format_space_utilization_empty(self):
        """Test space utilization at 0%"""
        result = format_space_utilization(0, 42)
        self.assertEqual(result, "0U / 42U (0.0%)")

    def test_format_space_utilization_zero_total(self):
        """Test space utilization with zero total (edge case)"""
        result = format_space_utilization(0, 0)
        self.assertEqual(result, "0U / 0U (0.0%)")

    def test_format_space_utilization_fractional(self):
        """Test space utilization with fractional percentage"""
        result = format_space_utilization(10, 42)
        self.assertEqual(result, "10U / 42U (23.8%)")

    @override_settings(WATTS_TO_BTU=3.412)
    def test_calculate_heat_output_basic(self):
        """Test heat output calculation with basic values"""
        result = calculate_heat_output(1000)
        self.assertAlmostEqual(result, 3412.0, places=1)

    @override_settings(WATTS_TO_BTU=3.412)
    def test_calculate_heat_output_zero(self):
        """Test heat output calculation with zero watts"""
        result = calculate_heat_output(0)
        self.assertEqual(result, 0.0)

    @override_settings(WATTS_TO_BTU=3.412)
    def test_calculate_heat_output_large(self):
        """Test heat output calculation with large power draw"""
        result = calculate_heat_output(10000)
        self.assertAlmostEqual(result, 34120.0, places=1)

    @override_settings(WATTS_TO_BTU=3.5)
    def test_calculate_heat_output_custom_conversion(self):
        """Test heat output with custom WATTS_TO_BTU setting"""
        result = calculate_heat_output(100)
        self.assertEqual(result, 350.0)

    def test_calculate_heat_output_decimal(self):
        """Test heat output calculation with decimal watts"""
        with self.settings(WATTS_TO_BTU=3.412):
            result = calculate_heat_output(500.5)
            self.assertAlmostEqual(result, 1707.706, places=2)


@pytest.mark.parametrize("watts,expected", [
    (0, "0 W (0.00 kW)"),
    (1, "1 W (0.00 kW)"),
    (999, "999 W (1.00 kW)"),
    (1000, "1,000 W (1.00 kW)"),
    (1500, "1,500 W (1.50 kW)"),
    (10000, "10,000 W (10.00 kW)"),
    (100000, "100,000 W (100.00 kW)"),
])
def test_format_power_parametrized(watts, expected):
    """Parametrized tests for power formatting"""
    assert format_power(watts) == expected


@pytest.mark.parametrize("used,total,expected", [
    (0, 42, "0U / 42U (0.0%)"),
    (21, 42, "21U / 42U (50.0%)"),
    (42, 42, "42U / 42U (100.0%)"),
    (10, 42, "10U / 42U (23.8%)"),
    (1, 3, "1U / 3U (33.3%)"),
])
def test_format_space_utilization_parametrized(used, total, expected):
    """Parametrized tests for space utilization formatting"""
    assert format_space_utilization(used, total) == expected

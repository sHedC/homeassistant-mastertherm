"""Test the Diagnostics."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.config_flow import DOMAIN
from custom_components.mastertherm.diagnostics import async_get_config_entry_diagnostics

from .conftest import APIMock


async def test_diagnostics(hass: HomeAssistant, mock_configdata: dict):
    """Test Diagnostics work."""
    api_mock = APIMock()
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.connect",
        side_effect=api_mock.connect,
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.refresh",
        side_effect=api_mock.refresh,
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.get_devices",
        side_effect=api_mock.get_devices,
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.get_device_data",
        side_effect=api_mock.get_device_data,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        diag_data = await async_get_config_entry_diagnostics(hass, entry)

        assert diag_data["config_entry_data"] == {
            "username": "**REDACTED**",
            "password": "**REDACTED**",
            "api_version": "v1",
        }
        assert "1112" in diag_data["coordinator_data"]["modules"]

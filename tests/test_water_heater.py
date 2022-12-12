"""Mastertherm Water Heater Tests."""
from unittest.mock import patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN

from .conftest import APIMock


@pytest.fixture(autouse=True)
def override_platform():
    """Override the Platforms to test Water Heater."""
    with patch("custom_components.mastertherm.PLATFORMS", [Platform.WATER_HEATER]):
        yield


async def test_water_heater_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
):
    """Test Water Heaters are Created and Updated."""
    api_mock = APIMock()
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    # Patch the Autentication and setup the entry.
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

    assert (
        hass.states.async_entity_ids_count(Platform.WATER_HEATER) > 0
    ), "Switches Failed to Create"

    # Check the Power Switch
    state = hass.states.get("water_heater.mt_1234_1_domestic_hot_water_enabled")
    assert state.state

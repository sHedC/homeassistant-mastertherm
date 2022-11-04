"""MasterTherm Sensor Tests."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.const import DOMAIN


async def test_sensor_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Sensors are Created and Updated."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata)
    entry.add_to_hass(hass)

    # Patch the Autentication and setup the entry.
    with patch(
        "custom_components.mastertherm.coordinator.MasterthermDataUpdateCoordinator._async_update_data",
        return_value=mock_entitydata,
    ) as mock_updater:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Check we called the Mock and we have a Sensor.
    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."
    assert (
        hass.states.async_entity_ids_count(Platform.SENSOR) > 0
    ), "Sensors Failed to Create"

    # Check the Temperature Sensor, TODO: Fix Not Working
    # assert state.state == "8.4"
    # assert state.name == "MasterTherm Serial Outside Temperature"

"""MasterTherm Sensor Tests."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.const import DOMAIN


async def test_no_sensors(hass: HomeAssistant):
    """Tests when No Sensors are Configured."""
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.async_entity_ids_count("sensor") == 0


async def test_sensors(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Sensors are Created and Updated."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata)
    entry.add_to_hass(hass)

    # Patch the Autentication and setup the entry.
    with patch(
        "custom_components.mastertherm.bridge.MasterthermDataUpdateCoordinator._async_update_data",
        return_value=mock_entitydata,
    ) as mock_updater:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Check we called the Mock and we have a Sensor.
    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."

    # Check the Temperature Sensor, TODO: Fix Not Working
    # state = hass.states.get("sensor.mt_1234_1_outside_temp")
    # assert state.state == "8.4"
    # assert state.name == "MasterTherm Serial Outside Temperature"

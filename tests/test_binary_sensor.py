"""Mastertherm Binary Sensor Tests."""
from unittest.mock import patch
import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN
from custom_components.mastertherm.entity_mappings import (
    MasterthermSelectEntityDescription,
)


@pytest.fixture(autouse=True)
def override_platform():
    """Override the ENTITIES to test Switches."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermSelectEntityDescription.__name__: Platform.BINARY_SENSOR},
    ):
        yield


async def test_binary_sensor_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Sensors are Created and Updated."""
    # Setting up using Mock requires the actual config not the Domain
    # changed the way the test works to send without domain.
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    # Patch the Autentication and setup the entry.
    with patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ) as mock_updater:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Check we called the Mock and we have a Sensor.
    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."
    assert (
        hass.states.async_entity_ids_count(Platform.BINARY_SENSOR) > 0
    ), "Binary Sensors Failed to Create"

    # Check the Temperature Sensor
    state = hass.states.get("binary_sensor.mt_1234_1_compressor_running")
    assert state.state
    assert state.name == "Compressor"

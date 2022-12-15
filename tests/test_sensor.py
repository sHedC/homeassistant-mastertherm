"""MasterTherm Sensor Tests."""
from unittest.mock import patch
import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN
from custom_components.mastertherm.entity_mappings import (
    MasterthermSensorEntityDescription,
)

from .conftest import APIMock


@pytest.fixture(autouse=True)
def override_platform():
    """Override the Platforms to test Switches."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermSensorEntityDescription.__name__: Platform.SENSOR},
    ):
        yield


async def test_sensor_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
):
    """Test Sensors are Created and Updated."""
    # Setting up using Mock requires the actual config not the Domain
    # changed the way the test works to send without domain.
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

    # Check we called the Mock and we have a Sensor.
    assert (
        hass.states.async_entity_ids_count(Platform.SENSOR) > 0
    ), "Sensors Failed to Create"

    # Check the Temperature Sensor
    state = hass.states.get("sensor.mt_1234_1_outside_temp")
    assert state.state == "2.7"
    assert state.name == "Outside Temperature"

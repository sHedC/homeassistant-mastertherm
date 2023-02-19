"""MasterTherm Climate Tests."""
from unittest.mock import patch
import pytest

from homeassistant.components.climate import (
    DOMAIN as CLIMATE_DOMAIN,
    SERVICE_SET_TEMPERATURE,
    SERVICE_SET_HVAC_MODE,
    ATTR_HVAC_MODE,
    HVACMode,
)
from homeassistant.const import Platform, ATTR_ENTITY_ID, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.const import (
    DOMAIN,
    MasterthermClimateEntityDescription,
)

from .conftest import APIMock


@pytest.fixture(autouse=True)
def override_entity():
    """Override the ENTITIES to test Climate."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermClimateEntityDescription.__name__: Platform.CLIMATE},
    ), patch(
        "custom_components.mastertherm.coordinator.ENTITIES",
        {MasterthermClimateEntityDescription.__name__: Platform.CLIMATE},
    ):
        yield


async def test_climate_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test Climate Entities are Created and Updated."""
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
            hass.states.async_entity_ids_count(Platform.CLIMATE) > 0
        ), "Climate Entities Failed to Create"

        # Check the Temperature Sensor
        state = hass.states.get("climate.mt_1234_1_heating_circuits_hc1_thermostat")
        assert state.attributes.get("current_temperature") == 20.0
        assert state.attributes.get("temperature") == 20.0


async def test_climate_update(hass: HomeAssistant, mock_configdata: dict):
    """Test Climate Entities are UPdated."""
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
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.set_device_data_item",
        side_effect=api_mock.set_device_data_item,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.mt_1234_1_heating_circuits_hc1_thermostat",
                ATTR_TEMPERATURE: 20.2,
            },
            blocking=True,
        )
        await hass.async_block_till_done()

        state = hass.states.get("climate.mt_1234_1_heating_circuits_hc1_thermostat")
        assert state.attributes.get("temperature") == 20.2


async def test_hvac_update(hass: HomeAssistant, mock_configdata: dict):
    """Test Climate Entity HVAC is updated."""
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
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController.set_device_data_item",
        side_effect=api_mock.set_device_data_item,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.mt_1234_2_heating_circuits_hc1_thermostat",
                ATTR_HVAC_MODE: HVACMode.AUTO,
            },
            blocking=True,
        )
        await hass.async_block_till_done()

        state = hass.states.get("climate.mt_1234_2_heating_circuits_hc1_thermostat")
        hvac = state.state

        assert hvac == HVACMode.AUTO

"""Mastertherm Switch Tests."""
from unittest.mock import patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    SERVICE_SET_VALUE,
)
from homeassistant.const import Platform, ATTR_ENTITY_ID

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN
from custom_components.mastertherm.entity_mappings import (
    MasterthermNumberEntityDescription,
)

from .conftest import APIMock


@pytest.fixture(autouse=True)
def override_entity():
    """Override the ENTITIES to test Numbers."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermNumberEntityDescription.__name__: Platform.NUMBER},
    ), patch(
        "custom_components.mastertherm.coordinator.ENTITIES",
        {MasterthermNumberEntityDescription.__name__: Platform.NUMBER},
    ):
        yield


@pytest.mark.skip(reason="No Entities Set Up Yes.")
async def test_number_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
):
    """Test Number Entities are Created and Updated."""
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

    # Check we called the Mock and we have an entity.
    assert (
        hass.states.async_entity_ids_count(Platform.NUMBER) > 0
    ), "Numbers Failed to Create"

    # Check the Power Switch
    state = hass.states.get("number.mt_1234_1_heating_circuits_hc1_ambient_requested")
    assert state.state == "20.0"
    assert state.name == "HC1 Ambient Requested"


@pytest.mark.skip(reason="No Entities Set Up Yes.")
async def test_set_temp(
    hass: HomeAssistant,
    mock_configdata: dict,
):
    """Test switching on updates."""
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
            NUMBER_DOMAIN,
            SERVICE_SET_VALUE,
            {
                ATTR_ENTITY_ID: "number.mt_1234_1_heating_circuits_hc1_ambient_requested",
                "value": 20.2,
            },
            blocking=True,
        )
        await hass.async_block_till_done()

    state = hass.states.get("number.mt_1234_1_heating_circuits_hc1_ambient_requested")
    assert state.state == "20.2"

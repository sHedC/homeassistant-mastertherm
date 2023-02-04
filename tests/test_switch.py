"""Mastertherm Switch Tests."""
from unittest.mock import patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from homeassistant.const import (
    Platform,
    ATTR_ENTITY_ID,
    STATE_ON,
    STATE_OFF,
)

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import (
    DOMAIN,
    MasterthermSwitchEntityDescription,
)

from .conftest import APIMock


@pytest.fixture(autouse=True)
def override_entity():
    """Override the ENTITIES to test Switches."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermSwitchEntityDescription.__name__: Platform.SWITCH},
    ), patch(
        "custom_components.mastertherm.coordinator.ENTITIES",
        {MasterthermSwitchEntityDescription.__name__: Platform.SWITCH},
    ):
        yield


async def test_switch_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Switches are Created and Updated."""
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
        hass.states.async_entity_ids_count(Platform.SWITCH) > 0
    ), "Switches Failed to Create"

    # Check the Power Switch
    state = hass.states.get("switch.mt_1234_1_hp_power_state")
    assert state.state
    assert state.name == "HP Power"


async def test_switch_on(
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

        state = hass.states.get("switch.mt_1234_1_hp_power_state")
        assert state.state == STATE_ON

        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_OFF,
            {ATTR_ENTITY_ID: "switch.mt_1234_1_hp_power_state"},
            blocking=True,
        )
        await hass.async_block_till_done()

    state = hass.states.get("switch.mt_1234_1_hp_power_state")
    assert state.state == STATE_OFF


async def test_dot_switch_on(
    hass: HomeAssistant,
    mock_configdata: dict,
):
    """Test switching parent child on works."""
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

        state = hass.states.get("switch.mt_1234_1_heating_circuits_hc1_on")
        assert state.state == STATE_OFF

        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: "switch.mt_1234_1_heating_circuits_hc1_on"},
            blocking=True,
        )
        await hass.async_block_till_done()

    state = hass.states.get("switch.mt_1234_1_heating_circuits_hc1_on")
    assert state.state == STATE_ON

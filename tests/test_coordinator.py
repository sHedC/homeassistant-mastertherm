"""Test the Coordinator Bridge."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import UpdateFailed

from pytest_homeassistant_custom_component.common import MockConfigEntry

from masterthermconnect import MasterthermTokenInvalid

from custom_components.mastertherm.config_flow import DOMAIN
from custom_components.mastertherm.coordinator import MasterthermDataUpdateCoordinator

from .conftest import APIMock


async def test_coordinator_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test the Coordinator."""
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

    assert hass.states.async_entity_ids_count(Platform.SENSOR) > 0


async def test_multiple_token_failures(hass: HomeAssistant, mock_configdata: dict):
    """Test that multiple token failures are handled correctly."""
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

    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Test token failure does not crash but re-tries
    with patch(
        "custom_components.mastertherm.coordinator.MasterthermController.refresh",
        side_effect=MasterthermTokenInvalid("3", "grr"),
    ):
        await coordinator.async_refresh()
        await hass.async_block_till_done()

    assert not isinstance(coordinator.last_exception, UpdateFailed)


async def test_pump_offline(hass: HomeAssistant, mock_configdata: dict):
    """Test when pump offline show pump offline and other entities unavailable."""
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

        coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][
            entry.entry_id
        ]

        api_mock.error = "offline"
        await coordinator.async_refresh()
        await hass.async_block_till_done()

    entity = hass.states.get("sensor.mt_1234_1_operating_mode")
    assert entity.state == "offline"

    entity = hass.states.get("switch.mt_1234_1_hp_power_state")
    assert entity.state == "unavailable"

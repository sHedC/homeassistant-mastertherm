"""Mastertherm Switch Tests."""
from unittest.mock import patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN


@pytest.fixture(autouse=True)
def override_platform():
    """Override the Platforms to test Switches."""
    with patch("custom_components.mastertherm.PLATFORMS", [Platform.SWITCH]):
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

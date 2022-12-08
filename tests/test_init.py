"""Test mastertherm setup process."""
from unittest.mock import patch

from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm import (
    async_setup_entry,
    async_reload_entry,
    async_unload_entry,
    MasterthermDataUpdateCoordinator,
)
from custom_components.mastertherm.const import DOMAIN


async def test_setup_unload_and_reload_entry(
    hass: HomeAssistant, mock_configdata: dict, mock_entitydata: dict
):
    """Test a Configured Instance that Logs In and Updates."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    with patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ) as mock_sync:
        assert await async_setup_entry(hass, entry)

        assert (
            len(hass.config_entries.flow.async_progress()) == 0
        ), "Flow is in Progress it should not be."

        assert DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]
        assert isinstance(
            hass.data[DOMAIN][entry.entry_id], MasterthermDataUpdateCoordinator
        )

        # Reload the entry and assert that the data from above is still there
        assert await async_reload_entry(hass, entry) is None
        assert DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]
        assert isinstance(
            hass.data[DOMAIN][entry.entry_id], MasterthermDataUpdateCoordinator
        )

    assert len(mock_sync.mock_calls) > 0

    # Unload the entry and verify that the data has been removed
    assert await async_unload_entry(hass, entry)
    assert entry.entry_id not in hass.data[DOMAIN]


async def test_unload_entry(
    hass: HomeAssistant, mock_configdata: dict, mock_entitydata: dict
):
    """Test being able to unload an entry, may fail is PLATFORM is setup and
    sensors fail to set up."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=mock_configdata[DOMAIN], entry_id="test"
    )
    entry.add_to_hass(hass)

    # Check the Config is initiated
    with patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ) as mock_updater:
        assert (
            await hass.config_entries.async_setup(entry.entry_id) is True
        ), "Component did not setup correctly."
        await hass.async_block_till_done()

    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."

    # Perform and Check Unload Config
    assert (
        await hass.config_entries.async_unload(entry.entry_id) is True
    ), "Component Config Unload Failed."
    assert entry.state == ConfigEntryState.NOT_LOADED

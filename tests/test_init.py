"""Test mastertherm setup process."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.config_entries import ConfigEntryState
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SOURCE,
    CONF_USERNAME,
)

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.const import DOMAIN


async def test_setup_with_no_config(hass: HomeAssistant):
    """Test the component gets setup without config."""
    assert await async_setup_component(hass, domain=DOMAIN, config={}) is True
    assert len(hass.config_entries.flow.async_progress()) == 0
    assert hass.data[DOMAIN] == {}


async def test_setup_valid(hass: HomeAssistant, mock_configdata, mock_entitydata):
    """Test a Configured Instance that Logs In and Updates."""

    # Patch the Autentication and setup the entry.
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ):
        assert (
            await async_setup_component(hass, domain=DOMAIN, config=mock_configdata)
            is True
        ), "Setup Component Failed."
        await hass.async_block_till_done()

    assert (
        len(hass.config_entries.flow.async_progress()) == 0
    ), "Flow is in Progress it should not be."

    # Locate the Config Entry and check the results
    for entry in hass.config_entries.async_entries(DOMAIN):
        if mock_configdata[DOMAIN][CONF_USERNAME] == entry.title:
            found_entry = entry

    assert (
        found_entry.title == mock_configdata[DOMAIN][CONF_USERNAME]
    ), "Entry is not setup."
    assert found_entry.data[CONF_USERNAME] == mock_configdata[DOMAIN][CONF_USERNAME]


async def test_setup_authenticationerror(hass: HomeAssistant, mock_configdata: dict):
    """Test a Configured Instance where Invalid Authentication is returned."""
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "authentication_error"},
    ) as mock_validation:
        assert (
            await async_setup_component(hass, domain=DOMAIN, config=mock_configdata)
            is True
        )

    assert len(mock_validation.mock_calls) == 1, "Mock Validation Failed"
    assert not hass.data.get(DOMAIN)


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


async def test_setup_twovalidentries(
    hass: HomeAssistant, mock_configdata: dict, mock_entitydata: dict
):
    """Test two valid configurations, two user accounts."""
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ):
        await async_setup_component(hass, domain=DOMAIN, config=mock_configdata)
        await hass.config_entries.flow.async_init(
            DOMAIN,
            context={CONF_SOURCE: SOURCE_IMPORT},
            data={
                CONF_USERNAME: "user.name2",
                CONF_PASSWORD: "hash2",
            },
        )
        await hass.async_block_till_done()

    # Locate our Entries
    for entry in hass.config_entries.async_entries(DOMAIN):
        if mock_configdata[DOMAIN][CONF_USERNAME] == entry.title:
            first_entry = entry
        if "user.name2" == entry.title:
            second_entry = entry

    assert first_entry.title == mock_configdata[DOMAIN][CONF_USERNAME]
    assert second_entry.title == "user.name2"

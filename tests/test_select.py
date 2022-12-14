"""Mastertherm Select Tests."""
from unittest.mock import patch

import pytest

from homeassistant.components.select import (
    SelectEntity,
    ATTR_OPTION,
    DOMAIN as SELECT_DOMAIN,
    SERVICE_SELECT_OPTION,
)
from homeassistant.const import Platform, ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.mastertherm.const import DOMAIN
from custom_components.mastertherm.entity_mappings import (
    MasterthermSelectEntityDescription,
)
from custom_components.mastertherm.coordinator import MasterthermDataUpdateCoordinator


@pytest.fixture(autouse=True)
def override_entity():
    """Override the ENTITIES to test Selects."""
    with patch(
        "custom_components.mastertherm.ENTITIES",
        {MasterthermSelectEntityDescription.__name__: Platform.SELECT},
    ), patch(
        "custom_components.mastertherm.coordinator.ENTITIES",
        {MasterthermSelectEntityDescription.__name__: Platform.SELECT},
    ):
        yield


async def test_select_setup(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Select Entities are Created"""
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

    # Check we called the Mock and we have a Select.
    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."
    assert (
        hass.states.async_entity_ids_count(Platform.SELECT) > 0
    ), "Selects Failed to Create"

    # Check the HP Function Select
    state: SelectEntity = hass.states.get("select.mt_1234_1_hp_function")
    assert state.state == "heating"
    assert state.name == "HP Function"


async def test_select_change(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test Select are not allowed to change, not working as comes back unavailable."""
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

    # Check we called the Mock and we have a Select.
    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."

    # Check the HP Function Select
    state: SelectEntity = hass.states.get("select.mt_1234_1_hp_function")
    assert state.state == "heating"

    await hass.services.async_call(
        SELECT_DOMAIN,
        SERVICE_SELECT_OPTION,
        {ATTR_OPTION: "auto", ATTR_ENTITY_ID: "select.mt_1234_1_hp_function"},
        blocking=True,
    )
    await hass.async_block_till_done()

    state: SelectEntity = hass.states.get("select.mt_1234_1_hp_function")
    assert state.state == "auto"

    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_refresh()
    await hass.async_block_till_done()

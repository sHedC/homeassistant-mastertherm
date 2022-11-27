"""Test the Coordinator Bridge"""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.setup import async_setup_component

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.config_flow import DOMAIN

from .conftest import APIMock


async def test_coordinator_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test the Coordinator"""
    # username = os.environ.get("MASTERTHERM_USER")
    # password = os.environ.get("MASTERTHERM_PASS")
    api_mock = APIMock()
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController",
        return_value=api_mock,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert hass.states.async_entity_ids_count(Platform.SENSOR) > 0

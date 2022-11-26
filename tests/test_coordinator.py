"""Test the Coordinator Bridge"""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.setup import async_setup_component

from custom_components.mastertherm.config_flow import DOMAIN

from .conftest import APIMock


async def test_coordinator_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test the Coordinator"""
    # username = os.environ.get("MASTERTHERM_USER")
    # password = os.environ.get("MASTERTHERM_PASS")
    api_mock = APIMock()

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch(
        "custom_components.mastertherm.coordinator.MasterthermController",
        return_value=api_mock,
    ):
        await async_setup_component(
            hass,
            domain=DOMAIN,
            config=mock_configdata,
        )
        await hass.async_block_till_done()

    assert hass.states.async_entity_ids_count(Platform.SENSOR) > 0

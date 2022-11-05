"""Helper and wrapper classes for MasterTherm module."""
import logging

from datetime import timedelta
from masterthermconnect import (
    Controller as MasterThermController,
    MasterThermAuthenticationError,
    MasterThermConnectionError,
    MasterThermUnsupportedRole,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MasterthermDataUpdateCoordinator(DataUpdateCoordinator):
    """MasterTherm Device and Data Updater from single HTTPS Session."""

    def __init__(self, hass: HomeAssistant, username: str, password: str):
        """Initialise the MasterTherm Update Coordinator class."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

        websession = aiohttp_client.async_get_clientsession(hass)
        self._api: MasterThermController = MasterThermController(
            websession=websession, username=username, password=password
        )
        self.platforms = []

    async def _async_update_data(self):
        """Refresh the data from the API endpoint and process."""
        raise UpdateFailed("Connection Error")
        return {}


async def authenticate(hass: HomeAssistant, username: str, password: str) -> dict:
    """Validate the user input by connecting."""
    auth_result = {}
    websession = aiohttp_client.async_get_clientsession(hass)
    try:
        controller = MasterThermController(websession, username, password)
        await controller.connect(update_data=False)
        auth_result["status"] = "success"
    except MasterThermAuthenticationError as ex:
        _LOGGER.error("Invalid credentials: %s", ex)
        auth_result["status"] = "authentication_error"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message
    except MasterThermConnectionError as ex:
        _LOGGER.error("Unable to communicate with MasterTherm API: %s", ex)
        auth_result["status"] = "connection_error"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message
    except MasterThermUnsupportedRole as ex:
        _LOGGER.error("Unsupported role: %s", ex)
        auth_result["status"] = "unsupported_role"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message

    return auth_result

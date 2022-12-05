"""Helper and wrapper classes for MasterTherm module."""
import logging

from datetime import timedelta
from aiohttp import ClientSession

from masterthermconnect import (
    MasterthermController,
    MasterthermAuthenticationError,
    MasterthermConnectionError,
    MasterthermUnsupportedRole,
    MasterthermTokenInvalid,
    MasterthermResponseFormatError,
)

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MasterthermDataUpdateCoordinator(DataUpdateCoordinator):
    """MasterTherm Device and Data Updater from single HTTPS Session."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        password: str,
        api_version: str,
        scan_interval: int = 10,
    ):
        """Initialise the MasterTherm Update Coordinator class."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )

        self.session = ClientSession()

        self.mt_controller: MasterthermController = MasterthermController(
            username,
            password,
            self.session,
            api_version=api_version,
        )
        self.platforms = []
        self._modules = []

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.session.close()

    async def _async_update_data(self) -> dict:
        """Refresh the data from the API endpoint and process."""
        # Try to refresh, check for refresh issues
        try:
            if self.data is None:
                connected = await self.mt_controller.connect()

            connected = await self.mt_controller.refresh()

            if not connected:
                _LOGGER.error("Update Failed for unknown reason")
                raise UpdateFailed("unknown_reason")

        except MasterthermAuthenticationError as ex:
            _LOGGER.error("Invalid credentials: %s", ex)
            raise ConfigEntryAuthFailed("authentication_error") from ex
        except MasterthermConnectionError as ex:
            _LOGGER.error("Unable to communicate with MasterTherm API: %s", ex)
            raise UpdateFailed("connection_error") from ex
        except MasterthermUnsupportedRole as ex:
            _LOGGER.error("Unsupported role: %s", ex)
            raise UpdateFailed("unsupported_role") from ex
        except MasterthermTokenInvalid as ex:
            _LOGGER.error("Invalid Token: %s", ex)
            raise UpdateFailed("invalid_token") from ex
        except MasterthermResponseFormatError as ex:
            _LOGGER.error("Response Format Error: %s", ex)
            raise UpdateFailed("response_format_error") from ex

        # If first run then populate the Modules.
        result_data = self.data
        if result_data is None:
            result_data = {"modules": {}}
            devices = self.mt_controller.get_devices()
            for device_id, device in devices.items():
                result_data["modules"][device_id] = {"info": device}

        # Retrieve the data and merge into the current data set based
        # based on the sensor configuration.
        for device_id, device in result_data["modules"].items():
            device_data = self.mt_controller.get_device_data(
                device["info"]["module_id"], device["info"]["unit_id"]
            )

            # Process Device Data, to pick up entities. Probably end up mapping it?
            # Short term adding just the outside temperature.
            result_data["modules"][device_id]["entities"] = {
                "outside_temp": {
                    "type": "temperature",
                    "name": "Outside Temperature",
                    "state": device_data["outside_temp"],
                },
                "heatpump_on": {
                    "type": "power",
                    "name": "Heatpump On",
                    "state": device_data["hp_power_state"],
                },
            }

        return result_data


async def authenticate(username: str, password: str, api_version: str) -> dict:
    """Validate the user input by connecting."""
    auth_result = {}
    websession = ClientSession()
    try:
        controller: MasterthermController = MasterthermController(
            username, password, websession, api_version=api_version
        )
        await controller.connect()
        auth_result["status"] = "success"
    except MasterthermAuthenticationError as ex:
        _LOGGER.error("Invalid credentials: %s", ex)
        auth_result["status"] = "authentication_error"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message
    except MasterthermConnectionError as ex:
        _LOGGER.error("Unable to communicate with MasterTherm API: %s", ex)
        auth_result["status"] = "connection_error"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message
    except MasterthermUnsupportedRole as ex:
        _LOGGER.error("Unsupported role: %s", ex)
        auth_result["status"] = "unsupported_role"
        auth_result["error_code"] = ex.status
        auth_result["error_message"] = ex.message
    finally:
        await websession.close()

    return auth_result

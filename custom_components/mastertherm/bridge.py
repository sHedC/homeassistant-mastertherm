"""Helper and wrapper classes for MasterTherm module."""
import logging
import random

from datetime import timedelta
from masterthermconnect import (
    Controller as MasterThermController,
    MasterThermAuthenticationError,
    MasterThermConnectionError,
    MasterThermUnsupportedRole,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import CONF_ENTITIES
from homeassistant.core import HomeAssistant
from homeassistant.helpers import (
    aiohttp_client,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MasterthermDataUpdateCoordinator(DataUpdateCoordinator):
    """MasterTherm Device and Data Updater from single HTTPS Session."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        """Initialise the MasterTherm Update Coordinator class."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

        self.config_entry = config_entry
        self.hass = hass
        self.api = None

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        if self.config_entry == {}:
            return {}

        return {
            "modules": {
                "1234_1": {
                    "info": {
                        "module_id": "1234",
                        "user_name": "BLABLA",
                        "module_name": "1234_AQI4434344_BlaBla_EE_UK_Thermal",
                        "serial_number": "AQI4434344",
                        "module_type": "Thermal",
                        "location": "EE",
                        "country": "UK",
                        "mb_addr": "1",
                        "mb_name": "unknown",
                    },
                    "entities": {
                        "outside_temp": {
                            "type": "temperature",
                            "name": "Outside Temperature",
                            "state": round(random.uniform(-10.00, 30.00), 2),
                        }
                    },
                }
            }
        }


class MasterthermEntity(CoordinatorEntity[MasterthermDataUpdateCoordinator]):
    """Represents a MasterTherm Device."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_type: str,
        entity_key: str = None,
    ):
        super().__init__(coordinator)
        self._module_key = module_key
        self._entity_key = entity_key
        self.entity_id = (
            f"{entity_type}.mt-{self._module_key}-{self._entity_key}".lower()
        )

    @property
    def get_module(self) -> dict:
        """Get the data for this module"""
        return self.coordinator.data["modules"][self._module_key]

    @property
    def get_moduleinfo(self) -> dict:
        """Get the Information for this Module"""
        return self.get_module["info"]

    @property
    def get_entity(self):
        """Get the specifi Entity data"""
        return self.get_module[CONF_ENTITIES][self._entity_key]

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return f"mastertherm-{self._module_key}-{self._entity_key}".lower()

    @property
    def name(self):
        """Return the Entity Friendly Name."""
        return (
            "Mastertherm "
            + self.get_moduleinfo["serial_number"]
            + " "
            + self.get_entity["name"]
        )

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return DeviceInfo(
            identifiers={{DOMAIN, "test2"}},
            manufacturer="Mastertherm",
            model="TBD",
            name="Matertherm Device",
            sw_version="TBD",
            configuration_url="TBD",
        )


async def authenticate(
    hass: HomeAssistant, username: str, password: str
) -> tuple[dict, dict]:
    """Validate the user input by connecting."""
    info = {}
    auth_result = {}
    websession = aiohttp_client.async_get_clientsession(hass)
    try:
        controller = MasterThermController(websession, username, password)
        info = await controller.connect()
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

    return auth_result, info

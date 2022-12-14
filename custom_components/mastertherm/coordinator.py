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
from homeassistant.helpers.entity import EntityDescription
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .entity_mappings import ENTITY_TYPES_MAP, ENTITIES

_LOGGER = logging.getLogger(__name__)


class MasterthermDataUpdateCoordinator(DataUpdateCoordinator):
    """MasterTherm Device and Data Updater from single HTTPS Session."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        password: str,
        api_version: str,
        scan_interval: int,
    ):
        """Initialise the MasterTherm Update Coordinator class."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

        # Temporary Exception Handling
        self.temporary_exception = False

        self.session = ClientSession()
        self.mt_controller: MasterthermController = MasterthermController(
            username,
            password,
            self.session,
            api_version=api_version,
        )

        # Make sure the allowed refresh rate in the API is lower than what we want.
        if scan_interval < 100:
            self.mt_controller.set_refresh_rate(data_refresh_seconds=scan_interval - 10)
        else:
            self.mt_controller.set_refresh_rate(data_refresh_seconds=60)

        self.entity_types: dict[str, EntityDescription] = self.__build_entity_types(
            ENTITY_TYPES_MAP
        )
        self.platforms = []
        self._modules = []

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.session.close()

    def __build_entity_types(
        self, entity_map: dict, parent: str = ""
    ) -> dict[str, EntityDescription]:
        """Build a list of each entity type from the Main Entity Map, recursive method."""
        entity_list = {}
        for entity_type in ENTITIES.values():
            entity_list[entity_type] = {}

        # For each Map Entry passed to this method process.
        for entity_key, entity in entity_map.items():
            if isinstance(entity, dict):
                # If entity is of type dict assume its a child to process.
                entity_list_update = self.__build_entity_types(
                    entity_map[entity_key], f"{parent}{entity_key}."
                )

                # Merget the child entries back to the parent.
                for entity_type in ENTITIES.values():
                    entity_list[entity_type].update(entity_list_update[entity_type])
            else:
                # Add the entity to the relevant dot noted key.
                if type(entity).__name__ in ENTITIES:
                    entity_list[ENTITIES[type(entity).__name__]][
                        f"{parent}{entity_key}"
                    ] = entity

        return entity_list

    def __build_entities(self, parent: str, device_data: dict) -> dict:
        """Build the Entities in dot notation, this is a nested method."""
        return_data = {}

        for state_id, state_value in device_data.items():
            if not isinstance(state_value, dict):
                return_data[f"{parent}{state_id}"] = state_value
            else:
                return_data.update(
                    self.__build_entities(f"{parent}{state_id}.", state_value)
                )

        return return_data

    async def _async_update_data(self) -> dict:
        """Refresh the data from the API endpoint and process."""
        # Try to refresh, check for refresh issues
        try:
            if self.data is None or self.temporary_exception:
                connected = await self.mt_controller.connect()
                self.temporary_exception = False

            connected = await self.mt_controller.refresh()

            if not connected:
                _LOGGER.error("Update Failed for unknown reason")
                raise UpdateFailed("unknown_reason")

        except MasterthermAuthenticationError as ex:
            _LOGGER.error("Invalid credentials: %s", ex)
            raise ConfigEntryAuthFailed("authentication_error") from ex
        except MasterthermUnsupportedRole as ex:
            _LOGGER.error("Unsupported role: %s", ex)
            raise UpdateFailed("unsupported_role") from ex
        except MasterthermConnectionError as ex:
            _LOGGER.warning("Unable to communicate with MasterTherm API: %s", ex)
            self.temporary_exception = True
        except MasterthermTokenInvalid as ex:
            _LOGGER.warning("Invalid Token: %s", ex)
            self.temporary_exception = True
        except MasterthermResponseFormatError as ex:
            _LOGGER.warning("Response Format Error: %s", ex)
            self.temporary_exception = True

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

            # Process Device Data and populate the data to pass to the Entities
            if "entities" in result_data["modules"][device_id]:
                result_data["modules"][device_id]["entities"].update(
                    self.__build_entities("", device_data)
                )
            else:
                result_data["modules"][device_id]["entities"] = self.__build_entities(
                    "", device_data
                )

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

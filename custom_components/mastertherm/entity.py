"""Mastertherm base entities."""
import logging

from homeassistant.const import CONF_ENTITIES
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .coordinator import MasterthermDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__package__)


class MasterthermEntity(CoordinatorEntity[MasterthermDataUpdateCoordinator]):
    """Mastertherm based Entity."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        entity_description: EntityDescription,
        module_key: str,
        entity_key: str,
        entity_type: str,
    ):
        """Initialisation for all Mastertherm Entities"""
        super().__init__(coordinator)

        self._module_key = module_key
        self._entity_key = entity_key
        # self.entity_description = entity_description
        self._attr_device_class = entity_description.device_class
        self._attr_unit_of_measurement = entity_description.unit_of_measurement
        self._attr_name = entity_description.name
        self._attr_icon = entity_description.icon
        self._attr_unique_id = slugify(f"mt_{module_key}_{entity_key}")
        self.entity_id = f"{entity_type}.{self._attr_unique_id}"

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
    def device_info(self):
        """Return the device_info of the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._module_key)},
            name=self.get_moduleinfo["module_name"],
            manufacturer="Mastertherm",
            model=self.get_moduleinfo["hp_type"],
            configuration_url=self.get_moduleinfo["api_url"],
        )

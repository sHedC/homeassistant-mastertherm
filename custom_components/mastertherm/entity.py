"""Mastertherm base entities."""
from homeassistant.const import CONF_ENTITIES
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MasterthermDataUpdateCoordinator
from .const import DOMAIN


class MasterthermEntity(CoordinatorEntity[MasterthermDataUpdateCoordinator]):
    """Mastertherm based Entity."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
    ):
        """Initialisation for all Mastertherm Entities"""
        super().__init__(coordinator)

        self._module_key = module_key
        self._entity_key = entity_key  #
        self._attr_unique_id = (
            f"mastertherm_{module_key}_{entity_key}".replace(" ", "_")
            .replace("-", "_")
            .lower()
        )
        self.entity_id = f"sensor.{self._attr_unique_id}"
        self._attr_name = self.coordinator.data["modules"][self._module_key][
            "entities"
        ][self._entity_key]["name"]

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
            configuration_url="https://mastertherm.vip-it.cz/",
        )

"""Mastertherm base entities."""
import logging

from homeassistant.const import CONF_ENTITIES
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .coordinator import MasterthermDataUpdateCoordinator
from .const import DOMAIN, VERSION

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
        """Initialize class properties."""
        super().__init__(coordinator)

        self._module_key = module_key
        self._entity_key = entity_key
        self.entity_description = entity_description
        self._attr_unique_id = slugify(f"mt_{module_key}_{entity_key}")
        self.entity_id = f"{entity_type}.{self._attr_unique_id}"

        self.entities = self.coordinator.data["modules"][self._module_key]["entities"]

        # If the entity is found in existing entities, remove it.
        if entity_type in coordinator.old_entries:
            if self.entity_id in coordinator.old_entries[entity_type]:
                entity_ids: list[str] = coordinator.old_entries[entity_type]
                entity_index = entity_ids.index(self.entity_id)
                entity_ids.pop(entity_index)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.entities["operating_mode"] == "offline":
            return self._entity_key == "operating_mode"
        else:
            return self.coordinator.last_update_success

    @property
    def get_module(self) -> dict:
        """Get the data for this module."""
        return self.coordinator.data["modules"][self._module_key]

    @property
    def get_moduleinfo(self) -> dict:
        """Get the Information for this Module."""
        return self.get_module["info"]

    @property
    def get_entity(self):
        """Get the specifi Entity data."""
        return self.get_module[CONF_ENTITIES][self._entity_key]

    @property
    def device_info(self):
        """Return the device_info of the device."""
        hp_type_desc = "Not Available"
        hp_type = self.get_module[CONF_ENTITIES]["hp_type"]
        match hp_type:
            case 0:
                hp_type_desc = "Air Source A/W"
            case 1:
                hp_type_desc = "Ground Source G/W"
            case 2:
                hp_type_desc = "Water Source W/W"
            case 3:
                hp_type_desc = "DX Ground Source DX/W"
            case 4:
                hp_type_desc = "Air Source A/WR"
            case 5:
                hp_type_desc = "Ground Source G/WR"
            case 6:
                hp_type_desc = "Water Source W/WR"

        return DeviceInfo(
            identifiers={(DOMAIN, self._module_key)},
            name=f"Mastertherm HeatPump ({hp_type_desc})",
            model="HeatPump (" + self.get_moduleinfo["hp_type"] + ")",
            manufacturer="Mastertherm",
            configuration_url=self.get_moduleinfo["api_url"],
            sw_version=VERSION,
            hw_version=self.get_moduleinfo["output"],
            via_device=(DOMAIN, self.get_moduleinfo["version"]),
        )

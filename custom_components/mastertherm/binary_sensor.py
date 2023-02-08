"""Support for Mastertherm Binary Sensors."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import (
    async_get,
    async_entries_for_config_entry,
)

from .const import DOMAIN, MasterthermBinarySensorEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Build a list of existing entities
    entity_registry = async_get(hass)
    existing_entities: list[str] = []
    for entity in async_entries_for_config_entry(entity_registry, entry.entry_id):

        _LOGGER.warning("Binary Sensor Found: %s:%s", entity.entity_id, entity.platform)

        if entity.platform == Platform.BINARY_SENSOR:
            existing_entities.append(entity.entity_id)

    entities: list[BinarySensorEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.BINARY_SENSOR
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermBinarySensor(
                        coordinator, module_key, entity_key, entity_description
                    )
                )
                if entity_key in existing_entities:
                    existing_entities.pop(entity_key)

    _LOGGER.warning("Binary Sensor Remaining: %s", len(existing_entities))

    async_add_entities(entities, True)


class MasterthermBinarySensor(MasterthermEntity, BinarySensorEntity):
    """Representation of a MasterTherm Binary Sensor, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermBinarySensorEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.BINARY_SENSOR,
            entity_description=entity_description,
        )

    @property
    def is_on(self) -> bool:
        """Return the Value."""
        return self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]

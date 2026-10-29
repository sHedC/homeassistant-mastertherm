"""Support for Mastertherm Binary Sensors."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MasterthermBinarySensorEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Binary Sensors from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[BinarySensorEntity] = []
    for entity_key, entity_description in coordinator.get_entity_types(
        Platform.BINARY_SENSOR
    ).items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermBinarySensor(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.BINARY_SENSOR)


class MasterthermBinarySensor(MasterthermEntity, BinarySensorEntity):
    """Representation of a MasterTherm Binary Sensor, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermBinarySensorEntityDescription,
    ):
        """Initialize the binary sensor."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.BINARY_SENSOR,
            entity_description=entity_description,
        )

        self._update_binary_sensor_state()

    @callback
    def _update_binary_sensor_state(self) -> None:
        """Update the binary sensor state."""
        self._attr_is_on = self.coordinator.get_state(self._module_key, self._entity_key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update the state."""
        self._update_binary_sensor_state()
        self.async_write_ha_state()

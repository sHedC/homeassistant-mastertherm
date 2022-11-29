"""Support for Mastertherm Binary Sensors."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors: list[BinarySensorEntity] = []
    for module_key, module in coordinator.data["modules"].items():
        for entity_key, entity in module[CONF_ENTITIES].items():
            if entity["type"] == BinarySensorDeviceClass.POWER:
                sensors.append(
                    MasterthermBinarySensor(coordinator, module_key, entity_key)
                )

    async_add_entities(sensors, True)


class MasterthermBinarySensor(MasterthermEntity, BinarySensorEntity):
    """Representation of a MasterTherm Binary Sensor, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
    ):
        self._attr_device_class = BinarySensorDeviceClass.POWER
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type="binary_sensor",
        )

    @property
    def device_class(self) -> str:
        return BinarySensorDeviceClass.POWER

    @property
    def is_on(self) -> bool | None:
        """Return the Value."""
        return self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]["on"]

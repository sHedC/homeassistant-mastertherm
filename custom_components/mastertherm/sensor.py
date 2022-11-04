"""Support for the MasterTherm Sensors."""
from decimal import Decimal
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, DEVICE_CLASS_TEMPERATURE

from .const import DOMAIN
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

    # config flow sets this to either UUID, serial number or None
    if (unique_id := entry.unique_id) is None:
        unique_id = entry.entry_id

    sensors: list[SensorEntity] = []
    for module_key, module in coordinator.data["modules"].items():
        for entity_key, entity in module[CONF_ENTITIES].items():
            if entity["type"] == "temperature":
                sensors.append(
                    MasterthermSensor(unique_id, coordinator, module_key, entity_key)
                )

    async_add_entities(sensors, True)


class MasterthermSensor(MasterthermEntity, SensorEntity):
    """Representation of a MasterTherm Sensor, e.g. ."""

    def __init__(
        self,
        unique_id: str,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
    ):
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_unique_id = f"{unique_id}_{module_key}"
        super().__init__(
            coordinator=coordinator, module_key=module_key, entity_key=entity_key
        )

    @property
    def native_value(self) -> Decimal:
        return 1.0

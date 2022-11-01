"""Support for the MasterTherm Sensors."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_ENTITIES, DEVICE_CLASS_TEMPERATURE

from .const import DOMAIN
from .bridge import MasterthermDataUpdateCoordinator, MasterthermEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    instance: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    sensors: list[SensorEntity] = []
    for module_key, module in instance["coordinator"].data["modules"].items():
        for entity_key, entity in module[CONF_ENTITIES].items():
            if entity["type"] == "temperature":
                sensors.append(
                    MasterthermSensor(instance["coordinator"], module_key, entity_key)
                )

    async_add_entities(sensors, True)


class MasterthermSensor(MasterthermEntity, SensorEntity):
    """Representation of a MasterTherm Sensor, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
    ):
        """Initialise the MasterTherm Update Coordinator class."""
        super().__init__(coordinator, module_key, SENSOR_DOMAIN, entity_key)

    @property
    def device_class(self):
        if self.get_entity["type"] == "temperature":
            return DEVICE_CLASS_TEMPERATURE

        return DEVICE_CLASS_TEMPERATURE

    @property
    def native_value(self):
        return self.get_entity["state"]

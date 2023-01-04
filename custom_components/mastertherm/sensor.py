"""Support for the Mastertherm Sensors."""
from decimal import Decimal
from datetime import date, datetime
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.const import CONF_ENTITIES, TEMP_CELSIUS, Platform

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import MasterthermSensorEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.SENSOR
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermSensor(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)


class MasterthermSensor(MasterthermEntity, SensorEntity):
    """Representation of a MasterTherm Sensor, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSensorEntityDescription,
    ):
        self._icon_state_map = entity_description.icon_state_map

        if entity_description.device_class == SensorDeviceClass.TEMPERATURE:
            entity_description.unit_of_measurement = TEMP_CELSIUS

        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SENSOR,
            entity_description=entity_description,
        )

    @property
    def icon(self) -> str | None:
        """Set dynamic icons if available."""
        if self._icon_state_map:
            return self._icon_state_map[self.native_value]
        else:
            return self.entity_description.icon

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        return self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]

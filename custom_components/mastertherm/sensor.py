"""Support for the Mastertherm Sensors."""
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, UnitOfTemperature, Platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from propcache import cached_property

from .const import DOMAIN, MasterthermSensorEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Sensors from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for entity_key, entity_description in coordinator.get_entity_types(
        Platform.SENSOR
    ).items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermSensor(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.SENSOR)


class MasterthermSensor(MasterthermEntity, SensorEntity):
    """Representation of a MasterTherm Sensor, e.g. ."""

    _sensor_description: MasterthermSensorEntityDescription

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSensorEntityDescription,
    ):
        """Initialize the sensor."""
        self._sensor_description = entity_description
        self._icon_state_map = entity_description.icon_state_map

        if entity_description.device_class == SensorDeviceClass.TEMPERATURE:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_suggested_unit_of_measurement = UnitOfTemperature.CELSIUS

        self._attr_state_class = entity_description.state_class

        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SENSOR,
            entity_description=entity_description,
        )

        self._update_sensor_state()

    @callback
    def _update_sensor_state(self) -> None:
        """Update the sensor state."""
        self._attr_native_value = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]

    @cached_property[str | None]
    def icon(self) -> str | None:
        """Set dynamic icons if available."""
        state = self.native_value
        if self._icon_state_map and isinstance(state, str):
            return self._icon_state_map.get(state, self.entity_description.icon)
        return self.entity_description.icon

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update the state."""
        self._update_sensor_state()
        self.async_write_ha_state()

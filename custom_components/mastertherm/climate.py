"""Support for the Mastertherm Thermostats."""
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    ClimateEntityDescription,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, UnitOfTemperature, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup climate entities from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[ClimateEntity] = []
    for module_key, module in coordinator.data["modules"].items():
        entity_description = ClimateEntityDescription(
            key="room_thermostat", name="Room Thermostat"
        )
        entities.append(
            MasterthermClimate(
                coordinator, module_key, "room_thermostat", entity_description
            )
        )

    async_add_entities(entities, True)


class MasterthermClimate(MasterthermEntity, ClimateEntity):
    """Representation of a Mastertherm Climate, room thermostats."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: ClimateEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.CLIMATE,
            entity_description=entity_description,
        )

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_min_temp = 0.0
        self._attr_max_temp = 30.0
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TARGET_HUMIDITY
        )
        self._attr_hvac_modes = [HVACMode.AUTO]
        self._attr_hvac_mode = HVACMode.AUTO

    @property
    def current_humidity(self) -> int | None:
        return 45

    @property
    def target_humidity(self) -> int | None:
        return 45

    @property
    def current_temperature(self) -> float | None:
        return 19.2

    @property
    def target_temperature(self) -> float | None:
        return 22.3

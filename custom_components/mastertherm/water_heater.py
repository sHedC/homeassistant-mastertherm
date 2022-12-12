"""Support for the Mastertherm Water Heater."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
    STATE_HEAT_PUMP,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform, UnitOfTemperature

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import (
    WATER_HEATER_TYPES,
    MasterthermWaterHeaterEntityDescription,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WaterHeaterEntity] = []
    for entity_key, entity_description in WATER_HEATER_TYPES.items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermWaterHeater(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)


class MasterthermWaterHeater(MasterthermEntity, WaterHeaterEntity):
    """Representation of a Mastertherm Waterheater, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermWaterHeaterEntityDescription,
    ):
        self._attr_supported_features = (
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
        )
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.WATER_HEATER,
            entity_description=entity_description,
        )

    @property
    def current_operation(self) -> str | None:
        # if self.coordinator.data["modules"][self._module_key]["entities"][
        #    self._entity_key
        # ]["enabled"]:
        #    return STATE_HEAT_PUMP
        return STATE_HEAT_PUMP

    @property
    def current_temperature(self) -> float | None:
        # return self.coordinator.data["modules"][self._module_key]["entities"][
        #    self._entity_key
        # ]["current_temp"]
        return 41.2

    @property
    def target_temperature(self) -> float | None:
        # return self.coordinator.data["modules"][self._module_key]["entities"][
        #    self._entity_key
        # ]["required_temp"]
        return 44.5

    @property
    def target_temperature_low(self) -> float | None:
        # return self.coordinator.data["modules"][self._module_key]["entities"][
        #    self._entity_key
        # ]["min_temp"]
        return 45.0

    @property
    def target_temperature_high(self) -> float | None:
        # return self.coordinator.data["modules"][self._module_key]["entities"][
        #    self._entity_key
        # ]["max_temp"]
        return 10.0

"""Support for the Mastertherm Thermostats."""
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_ENTITIES,
    PRECISION_TENTHS,
    UnitOfTemperature,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MasterthermClimateEntityDescription
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
    for entity_key, entity_description in coordinator.entity_types[
        Platform.CLIMATE
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_description.key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermClimate(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.CLIMATE)


class MasterthermClimate(MasterthermEntity, ClimateEntity):
    """Representation of a Mastertherm Climate, room thermostats."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermClimateEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.CLIMATE,
            entity_description=entity_description,
        )

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = PRECISION_TENTHS
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

        self._current_temperature_path = entity_description.current_temperature_path
        self._target_temperature_path = entity_description.requested_temperature_path

        # Is HVAC Mode available or not.
        self._hvac_mode_enabled = False
        self._attr_hvac_modes = [HVACMode.OFF]
        self._power_state_path = entity_description.power_state_path
        if entity_description.power_state_path in self.entities:
            self._attr_hvac_modes = [HVACMode.OFF, HVACMode.AUTO]
            self._hvac_mode_enabled = True

        # if Min/ Max temp is a string then assume the value is looked up.
        if isinstance(entity_description.min_temp, str):
            self._attr_min_temp = self.entities[entity_description.min_temp]
        else:
            self._attr_min_temp = entity_description.min_temp
        if isinstance(entity_description.max_temp, str):
            self._attr_max_temp = self.entities[entity_description.max_temp]
        else:
            self._attr_max_temp = entity_description.max_temp

    @property
    def hvac_mode(self) -> HVACMode | str | None:
        """If HVACMode enabled then check what state"""
        # 0 is perm off, 1 or 2 is AUTO for on or scheduled off.
        hvac_mode = HVACMode.OFF
        if self._hvac_mode_enabled and self.entities[self._power_state_path] in [1, 2]:
            hvac_mode = HVACMode.AUTO

        return hvac_mode

    @property
    def current_temperature(self) -> float | None:
        return self.entities[self._current_temperature_path]

    @property
    def target_temperature(self) -> float | None:
        return self.entities[self._target_temperature_path]

    @property
    def target_temperature_step(self) -> float:
        """Set target temperature step to tenths."""
        return PRECISION_TENTHS

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs) -> None:
        """Write the updated temperature to mastertherm."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        await self.coordinator.update_state(
            self._module_key, self._target_temperature_path, temp
        )
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Currently this is not supported, display a warning."""
        if self._hvac_mode_enabled:
            if hvac_mode == HVACMode.OFF:
                await self.coordinator.update_state(
                    self._module_key, self._power_state_path, 0
                )
            elif self.entities[self._power_state_path] == 0:
                await self.coordinator.update_state(
                    self._module_key, self._power_state_path, 2
                )

        self.async_write_ha_state()

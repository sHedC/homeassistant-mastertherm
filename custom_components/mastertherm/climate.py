"""Support for the Mastertherm Thermostats."""

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
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
from propcache import cached_property

from .const import DOMAIN, MasterthermClimateEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load the Climate entity from the config entries."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[ClimateEntity] = []
    for entity_key, entity_description in coordinator.get_entity_types(
        Platform.CLIMATE
    ).items():
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

    _climate_description: MasterthermClimateEntityDescription

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermClimateEntityDescription,
    ):
        """Initialize the Climate Entries."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.CLIMATE,
            entity_description=entity_description,
        )

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = PRECISION_TENTHS
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )
        self._enable_turn_on_off_backwards_compatibility = False
        self._climate_description = entity_description

        # Is HVAC Mode available or not.
        self._hvac_mode_enabled = False
        self._attr_hvac_modes = [HVACMode.AUTO]
        if self._climate_description.power_state_path in self.entities:
            self._attr_hvac_modes = [HVACMode.OFF, HVACMode.AUTO]
            self._hvac_mode_enabled = True

        # if Min/ Max temp is a string then assume the value is looked up.
        if isinstance(self._climate_description.min_temp, str):
            self._attr_min_temp = self.entities[self._climate_description.min_temp]
        else:
            self._attr_min_temp = self._climate_description.min_temp
        if isinstance(self._climate_description.max_temp, str):
            self._attr_max_temp = self.entities[self._climate_description.max_temp]
        else:
            self._attr_max_temp = self._climate_description.max_temp

        self._update_climate_state()

    @callback
    def _update_climate_state(self) -> None:
        """Update cached climate attributes from coordinator data."""
        self._attr_current_temperature = self.entities[
            self._climate_description.current_temperature_path
        ]
        self._attr_target_temperature = self.entities[
            self._climate_description.requested_temperature_path
        ]

        if self._hvac_mode_enabled:
            if (
                self.entities[self._climate_description.power_state_path]
                != self._climate_description.power_state_off
            ):
                self._attr_hvac_mode = HVACMode.AUTO
            else:
                self._attr_hvac_mode = HVACMode.OFF
        else:
            self._attr_hvac_mode = HVACMode.AUTO

    @cached_property[float]
    def target_temperature_step(self) -> float:
        """Set target temperature step to tenths."""
        return PRECISION_TENTHS

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_climate_state()
        super()._handle_coordinator_update()

    async def async_set_temperature(self, **kwargs) -> None:
        """Write the updated temperature to mastertherm."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        await self.coordinator.update_state(
            self._module_key, self._climate_description.requested_temperature_path, temp
        )
        self._update_climate_state()
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC Mode."""
        if self._hvac_mode_enabled:
            if hvac_mode == HVACMode.OFF:
                await self.coordinator.update_state(
                    self._module_key,
                    self._climate_description.power_state_path,
                    self._climate_description.power_state_off,
                )
            elif (
                self.entities[self._climate_description.power_state_path]
                == self._climate_description.power_state_off
            ):
                await self.coordinator.update_state(
                    self._module_key,
                    self._climate_description.power_state_path,
                    self._climate_description.power_state_on,
                )

        self._update_climate_state()
        self.async_write_ha_state()

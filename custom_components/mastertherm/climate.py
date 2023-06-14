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
    """Load the Climate entity from the config entries."""
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
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
        self._descrption = entity_description

        # Is HVAC Mode available or not.
        self._hvac_mode_enabled = False
        self._attr_hvac_modes = [HVACMode.AUTO]
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
        """If HVACMode enabled then check what state."""
        # 0 is perm off, 1 or 2 is AUTO for on or scheduled off.
        if self._hvac_mode_enabled:
            if (
                self.entities[self._descrption.power_state_path]
                != self._descrption.power_state_off
            ):
                hvac_mode = HVACMode.AUTO
            else:
                hvac_mode = HVACMode.OFF
        else:
            hvac_mode = HVACMode.AUTO

        return hvac_mode

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self.entities[self._descrption.current_temperature_path]

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        return self.entities[self._descrption.requested_temperature_path]

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
            self._module_key, self._descrption.requested_temperature_path, temp
        )
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC Mode."""
        if self._hvac_mode_enabled:
            if hvac_mode == HVACMode.OFF:
                await self.coordinator.update_state(
                    self._module_key,
                    self._descrption.power_state_path,
                    self._descrption.power_state_off,
                )
            elif (
                self.entities[self._descrption.power_state_path]
                == self._descrption.power_state_off
            ):
                await self.coordinator.update_state(
                    self._module_key,
                    self._descrption.power_state_path,
                    self._descrption.power_state_on,
                )

        self.async_write_ha_state()

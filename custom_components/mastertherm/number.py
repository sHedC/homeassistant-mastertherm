"""Support for the Mastertherm Numbers."""
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform

from .const import DOMAIN, MasterthermNumberEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Number Sensors from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[NumberEntity] = []
    for entity_key, entity_description in coordinator.get_entity_types(
        Platform.NUMBER
    ).items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermNumber(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.NUMBER)


class MasterthermNumber(MasterthermEntity, NumberEntity):
    """Representation of a MasterTherm Switch, e.g. ."""

    _number_description: MasterthermNumberEntityDescription

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermNumberEntityDescription,
    ):
        """Initialize the number sensor."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.NUMBER,
            entity_description=entity_description,
        )
        self._number_description = entity_description

        self._attr_mode = self._number_description.mode
        if self._number_description.min_lookup:
            self._attr_native_min_value = self.coordinator.data["modules"][
                self._module_key
            ]["entities"][self._number_description.min_lookup]
        if self._number_description.max_lookup:
            self._attr_native_max_value = self.coordinator.data["modules"][
                self._module_key
            ]["entities"][self._number_description.max_lookup]

        self._update_number_state()

    @callback
    def _update_number_state(self) -> None:
        """Update the number state."""
        self._attr_native_value = self.coordinator.get_state(self._module_key, self._entity_key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update the state."""
        self._update_number_state()
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the Number Value."""
        await self.coordinator.update_state(self._module_key, self._entity_key, value)
        self._update_number_state()
        self.async_write_ha_state()

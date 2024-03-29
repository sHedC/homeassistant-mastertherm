"""Support for the Mastertherm Switches."""
import logging

from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform

from .const import DOMAIN, MasterthermSwitchEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Switches from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SwitchEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.SWITCH
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermSwitch(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.SWITCH)


class MasterthermSwitch(MasterthermEntity, SwitchEntity):
    """Representation of a MasterTherm Switch, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSwitchEntityDescription,
    ):
        """Initialize the switches."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SWITCH,
            entity_description=entity_description,
        )

        self._read_only = entity_description.read_only

    @property
    def is_on(self) -> bool | None:
        """Return if switch is on or off."""
        return self.coordinator.get_state(self._module_key, self._entity_key)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Update to turn on the given switch."""
        if not self._read_only:
            await self.coordinator.update_state(
                self._module_key, self._entity_key, True
            )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Reset the update, not supported at this time."""
        if not self._read_only:
            await self.coordinator.update_state(
                self._module_key, self._entity_key, False
            )
        self.async_write_ha_state()

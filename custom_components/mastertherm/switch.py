"""Support for the Mastertherm Switches."""
import logging

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import MasterthermSwitchEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
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


class MasterthermSwitch(MasterthermEntity, SwitchEntity):
    """Representation of a MasterTherm Switch, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSwitchEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SWITCH,
            entity_description=entity_description,
        )

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]

    def turn_on(self, **kwargs: Any) -> None:
        """Reset the update, not supported at this time."""
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs: Any) -> None:
        """Reset the update, not supported at this time."""
        self.schedule_update_ha_state()

"""Support for the Mastertherm Select."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, Platform
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import MasterthermSelectEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup select from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.SELECT
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermSelect(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)


class MasterthermSelect(MasterthermEntity, SelectEntity):
    """Representation of a MasterTherm Select, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSelectEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SELECT,
            entity_description=entity_description,
        )

        self._attr_options = entity_description.options
        if entity_description.options_map:
            self._options_map = entity_description.options_map
        else:
            for key in entity_description.options:
                self._options_map = {key: key}

        self._reverse_map = {val: key for key, val in self._options_map.items()}

        # Set Initial State
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        self._attr_current_option = self._reverse_map.get(state)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        self._attr_current_option = self._reverse_map.get(state)
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Update the Current Option, but don't send update."""
        self._attr_current_option = option
        self.async_write_ha_state()

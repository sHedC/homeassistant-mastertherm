"""Support for the Mastertherm Select."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, Platform
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MasterthermSelectEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Select entities from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.SELECT
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key == "season.select":
                entities.append(
                    MasterthermSeasonSelect(
                        coordinator, module_key, entity_key, entity_description
                    )
                )
            elif entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermSelect(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)
    coordinator.remove_old_entities(Platform.SELECT)


class MasterthermSelect(MasterthermEntity, SelectEntity):
    """Representation of a MasterTherm Select, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSelectEntityDescription,
    ):
        """Initialize the select sensor."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SELECT,
            entity_description=entity_description,
        )

        if entity_description.options_map:
            self._options_map = entity_description.options_map
        else:
            for key in entity_description.options:
                self._options_map = {key: key}

        self._reverse_map = {val: key for key, val in self._options_map.items()}

    @property
    def current_option(self) -> str | None:
        """Return the current select option."""
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        return self._reverse_map.get(state)

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
        value = self._options_map.get(option)
        await self.coordinator.update_state(self._module_key, self._entity_key, value)
        self.async_write_ha_state()


class MasterthermSeasonSelect(MasterthermEntity, SelectEntity):
    """Special Class for Mastertherm Season Select, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermSelectEntityDescription,
    ):
        """Initialize the season sensor."""
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.SELECT,
            entity_description=entity_description,
        )

    @property
    def current_option(self) -> str | None:
        """Return the current season option."""
        entities = self.coordinator.data["modules"][self._module_key]["entities"]
        if entities["season.manual_set"]:
            return "winter" if entities["season.winter"] else "summer"
        else:
            return "auto"

    async def async_select_option(self, option: str) -> None:
        """Update the Current Option, but don't send update."""
        if option == "auto":
            await self.coordinator.update_state(
                self._module_key, "season.manual_set", False
            )
        elif option == "winter":
            await self.coordinator.update_state(
                self._module_key, "season.manual_set", True
            )
            await self.coordinator.update_state(self._module_key, "season.winter", True)
        else:
            await self.coordinator.update_state(
                self._module_key, "season.manual_set", True
            )
            await self.coordinator.update_state(
                self._module_key, "season.winter", False
            )

        self.async_write_ha_state()

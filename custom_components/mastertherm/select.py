"""Support for the Mastertherm Select."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import SELECT_TYPES, MasterthermSelectEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup select from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = []
    for entity_key, entity_description in SELECT_TYPES.items():
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

        if entity_description.options_map:
            self._options_map = entity_description.options_map
        else:
            for key in entity_description.options:
                self._options_map = {key: key}

        self._reverse_map = {val: key for key, val in self._options_map.items()}

    @property
    def current_option(self) -> str | None:
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        option = self._reverse_map.get(state)
        if option is not None:
            return option.lower()
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        option = self._reverse_map.get(state)
        await self.hass.async_add_executor_job(self.select_option, option)

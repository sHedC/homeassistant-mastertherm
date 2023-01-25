"""Support for the Mastertherm Numbers."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITIES, Platform

from .const import DOMAIN
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity
from .entity_mappings import MasterthermNumberEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup numbers from a config entry created in the integrations UI."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[NumberEntity] = []
    for entity_key, entity_description in coordinator.entity_types[
        Platform.NUMBER
    ].items():
        for module_key, module in coordinator.data["modules"].items():
            if entity_key in module[CONF_ENTITIES]:
                entities.append(
                    MasterthermNumber(
                        coordinator, module_key, entity_key, entity_description
                    )
                )

    async_add_entities(entities, True)


class MasterthermNumber(MasterthermEntity, NumberEntity):
    """Representation of a MasterTherm Switch, e.g. ."""

    def __init__(
        self,
        coordinator: MasterthermDataUpdateCoordinator,
        module_key: str,
        entity_key: str,
        entity_description: MasterthermNumberEntityDescription,
    ):
        super().__init__(
            coordinator=coordinator,
            module_key=module_key,
            entity_key=entity_key,
            entity_type=Platform.NUMBER,
            entity_description=entity_description,
        )

        self._attr_mode = ""

    @property
    def native_value(self) -> float:
        return self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]

    async def async_set_native_value(self, value: float) -> None:
        """Update the Number Value."""
        await self.coordinator.update_state(self._module_key, self._entity_key, value)
        self.async_write_ha_state()

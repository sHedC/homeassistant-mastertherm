"""Support for the Mastertherm Select."""


from homeassistant.core import HomeAssistant
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITIES, Platform
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MasterthermSelectEntityDescription
from .coordinator import MasterthermDataUpdateCoordinator
from .entity import MasterthermEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Load Select entities from the config settings."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = []
    for entity_key, entity_description in coordinator.get_entity_types(
        Platform.SELECT
    ).items():
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

    _select_description: MasterthermSelectEntityDescription

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
        self._select_description = entity_description

        if self._select_description.options is None:
            raise ValueError(f"Select entity {entity_key} must define options")

        if self._select_description.options_map:
            self._options_map = self._select_description.options_map
        else:
            self._options_map = {
                key: key for key in self._select_description.options
            }

        self._reverse_map = {val: key for key, val in self._options_map.items()}

        self._update_select_state()

    @callback
    def _update_select_state(self) -> None:
        """Update the select state."""
        state = self.coordinator.data["modules"][self._module_key]["entities"][
            self._entity_key
        ]
        self._attr_current_option = self._reverse_map.get(state)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_select_state()
        super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        """Update the Current Option, but don't send update."""
        value = self._options_map.get(option)
        await self.coordinator.update_state(self._module_key, self._entity_key, value)
        self._update_select_state()
        self.async_write_ha_state()


class MasterthermSeasonSelect(MasterthermEntity, SelectEntity):
    """Special Class for Mastertherm Season Select, e.g. ."""

    _select_description: MasterthermSelectEntityDescription

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

        self._select_description = entity_description

        self._update_select_state()

    @callback
    def _update_select_state(self) -> None:
        """Update the select state."""
        entities = self.coordinator.data["modules"][self._module_key]["entities"]
        if entities["season.manual_set"]:
            self._attr_current_option = (
                "winter" if entities["season.winter"] else "summer"
            )
        else:
            self._attr_current_option = "auto"

    async def async_select_option(self, option: str) -> None:
        """Update the Current Option, but don't send update."""
        if option == "auto":
            await self.coordinator.update_state(
                self._module_key, "season.manual_set", False
            )
        else:
            if self.coordinator.data["modules"][self._module_key]["entities"]["season.manual_set"] is False:
                await self.coordinator.update_state(
                    self._module_key, "season.manual_set", True
                )
            await self.coordinator.update_state(
                self._module_key, "season.winter", True if option == "winter" else False
            )

        self._update_select_state()
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update the state."""
        self._update_select_state()
        self.async_write_ha_state()

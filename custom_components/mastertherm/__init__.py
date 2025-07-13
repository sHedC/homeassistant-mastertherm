"""Mastertherm integration to integrate Mastertherm Heatpumps with Home Assistant."""

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_API_VERSION,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant

from .coordinator import MasterthermDataUpdateCoordinator
from .const import (
    CONF_FULL_REFRESH,
    CONF_REFRESH_OFFSET,
    DOMAIN,
    DEFAULT_REFRESH,
    DEFAULT_FULL_REFRESH,
    DEFAULT_REFRESH_OFFSET,
    ENTITIES,
)

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MasterTherm integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = MasterthermDataUpdateCoordinator(
        hass,
        config_entry=entry,
        username=entry.data.get(CONF_USERNAME),
        password=entry.data.get(CONF_PASSWORD),
        api_version=entry.data.get(CONF_API_VERSION),
        scan_interval=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH),
        full_refresh_interval=entry.options.get(CONF_FULL_REFRESH, DEFAULT_FULL_REFRESH),
        data_refresh_offset=entry.options.get(CONF_REFRESH_OFFSET, DEFAULT_REFRESH_OFFSET)
    )
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, ENTITIES.values())
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ENTITIES.values())


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

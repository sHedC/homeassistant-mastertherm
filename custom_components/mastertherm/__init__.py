"""Mastertherm integration to integrate Mastertherm Heatpumps with Home Assistant."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_API_VERSION,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity_registry import (
    async_get_registry,
    async_entries_for_config_entry,
)

from .coordinator import MasterthermDataUpdateCoordinator
from .const import DOMAIN, DEFAULT_REFRESH, ENTITIES

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(
    hass: HomeAssistant, config: Config
):  # pylint: disable=unused-argument
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MasterTherm integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    if not (coordinator := hass.data[DOMAIN].get(entry.entry_id)):
        # Initiate the Coordinator, not sure if I will need separate session for separate users
        username = entry.data.get(CONF_USERNAME)
        password = entry.data.get(CONF_PASSWORD)
        api_version = entry.data.get(CONF_API_VERSION)
        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH)
        coordinator = MasterthermDataUpdateCoordinator(
            hass,
            username,
            password,
            api_version,
            scan_interval,
        )
        hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()
    if not coordinator.data:
        raise ConfigEntryNotReady

    entity_registry = await async_get_registry(hass)
    entities = async_entries_for_config_entry(entity_registry, entry.entry_id)
    _LOGGER.warning("Entities Loaded %s", len(entities))

    for platform in ENTITIES.values():
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ENTITIES)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

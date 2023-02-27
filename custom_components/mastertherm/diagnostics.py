"""Diagnostics support for Mastertherm"""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.core import HomeAssistant

from . import MasterthermDataUpdateCoordinator
from .const import DOMAIN

TO_REDACT = {
    CONF_USERNAME,
    CONF_PASSWORD,
    "module_id",
    "name",
    "module_name",
    "surname",
    "notes",
    CONF_LATITUDE,
    CONF_LONGITUDE,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: MasterthermDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    api_diagnostic = coordinator.mt_controller.get_diagnostics_data()

    # Make coordinator data anoymous
    new_id = 1111
    coordinator_data = {"modules": {}}
    for device_info in dict(coordinator.data)["modules"].values():
        new_id = new_id + 1
        coordinator_data["modules"][str(new_id)] = device_info

    diagnostics_data = {
        "config_entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "coordinator_data": async_redact_data(dict(coordinator_data), TO_REDACT),
        "api_data": api_diagnostic,
    }

    return diagnostics_data

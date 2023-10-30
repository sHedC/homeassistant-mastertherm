"""Constants used by Home Assistant Components."""
from dataclasses import dataclass, field

from homeassistant.const import Platform, UnitOfTemperature
from homeassistant.components.climate import (
    ClimateEntityDescription,
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
)
from homeassistant.components.number import NumberEntityDescription, NumberDeviceClass
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.switch import SwitchEntityDescription

NAME = "Mastertherm"
DOMAIN = "mastertherm"
VERSION = "1.1.7-b1"

API_VERSIONS = {
    "v1": "mastertherm.vip-it.cz (< 2022)",
    "v2": "mastertherm.online (> 2022)",
}

# Default Refresh Rate in Seconds
DEFAULT_REFRESH = 120
DEFAULT_FULL_REFRESH = 15
DEFAULT_REFRESH_OFFSET = 5

CONF_FULL_REFRESH = "full_refresh_interval"
CONF_REFRESH_OFFSET = "data_refresh_offset"


@dataclass
class MasterthermBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Description for the Mastertherm binary sensor entities."""


@dataclass
class MasterthermClimateEntityDescription(ClimateEntityDescription):
    """Description for the Mastertherm Climate Entity."""

    # Key must be the entity that decides if this is enabled
    # in dot notation e.g. heating_circuits.hc1.ambient_requested
    # current_temperature_path and requested_temperature_path are
    # the entities to lookup the states in dot notation as above.
    current_temperature_path: str = None
    requested_temperature_path: str = None
    power_state_path: str = None
    power_state_on: int | bool | None = None
    power_state_off: int | bool | None = None
    min_temp: float | str = DEFAULT_MIN_TEMP
    max_temp: float | str = DEFAULT_MAX_TEMP


@dataclass
class MasterthermNumberEntityDescription(NumberEntityDescription):
    """Description for the Mastertherm Number Entity."""

    device_class = NumberDeviceClass.TEMPERATURE
    native_unit_of_measurement = UnitOfTemperature.CELSIUS
    native_step: float = 0.5
    mode: str = "auto"

    min_lookup: str = None
    max_lookup: str = None


@dataclass
class MasterthermSelectEntityDescription(SelectEntityDescription):
    """Description for the Mastertherm select entities."""

    options_map: dict = field(default_factory=dict)
    read_only: bool = False


@dataclass
class MasterthermSensorEntityDescription(SensorEntityDescription):
    """Description for the Mastertherm sensor entities."""

    icon_state_map: dict[str, str] = field(default_factory=dict[str, str])


@dataclass
class MasterthermSwitchEntityDescription(SwitchEntityDescription):
    """Description for the Mastertherm switch entities."""

    read_only: bool = False


ENTITIES: dict[str, str] = {
    MasterthermBinarySensorEntityDescription.__name__: Platform.BINARY_SENSOR,
    MasterthermSelectEntityDescription.__name__: Platform.SELECT,
    MasterthermSensorEntityDescription.__name__: Platform.SENSOR,
    MasterthermSwitchEntityDescription.__name__: Platform.SWITCH,
    MasterthermClimateEntityDescription.__name__: Platform.CLIMATE,
    MasterthermNumberEntityDescription.__name__: Platform.NUMBER,
}

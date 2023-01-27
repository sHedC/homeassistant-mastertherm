"""Contains all the Entity Mappings from the Mastertherm Connector"""
from dataclasses import dataclass, field

from homeassistant.components.climate import (
    ClimateEntityDescription,
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
)
from homeassistant.components.number import (
    NumberEntityDescription,
    NumberDeviceClass,
)
from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)
from homeassistant.components.select import (
    SelectEntityDescription,
)
from homeassistant.components.switch import (
    SwitchEntityDescription,
    SwitchDeviceClass,
)
from homeassistant.const import Platform, PERCENTAGE, TIME_HOURS, UnitOfTemperature


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
    min_temp: int = DEFAULT_MIN_TEMP
    max_temp: int = DEFAULT_MAX_TEMP


@dataclass
class MasterthermNumberEntityDescription(NumberEntityDescription):
    """Description for the Mastertherm Number Entity."""

    read_only: bool = False
    mode: str = "auto"


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

# Putting all entities into a single map which hopfully makes it easier
# to maintain, will split into usable entity lists in the coordinator.
HEATING_CIRCUITS: dict = {
    "hc0": {
        "name": MasterthermSensorEntityDescription(
            key="hc0_name",
            name="HC0 Name",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc0_ambient_requested",
            name="HC0 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc0_ambient_temp",
            name="HC0 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc0.ambient_requested",
            name="HC0 Thermostat",
            current_temperature_path="heating_circuits.hc0.ambient_temp",
            requested_temperature_path="heating_circuits.hc0.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc0_pad_current_humidity",
                name="HC0 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc1": {
        "name": MasterthermSensorEntityDescription(
            key="hc1_name",
            name="HC1 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc1_on",
            name="HC1",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc1_cooling",
            name="HC1 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc1_circulation_valve",
            name="HC1 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc1_water_requested",
            name="HC1 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc1_water_temp",
            name="HC1 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc1_auto",
            name="HC1 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc1_ambient_requested",
            name="HC1 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermNumberEntityDescription(
            key="hc1_ambient_temp",
            name="HC1 Ambient Temperature",
            device_class=NumberDeviceClass.TEMPERATURE,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc1.ambient_requested",
            name="HC1 Thermostat",
            current_temperature_path="heating_circuits.hc1.ambient_temp",
            requested_temperature_path="heating_circuits.hc1.ambient_requested",
        ),
        "pad": {
            "state": MasterthermSensorEntityDescription(
                key="hc1_pad_state",
                name="HC1 PAD State",
            ),
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc1_pad_current_humidity",
                name="HC1 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc2": {
        "name": MasterthermSensorEntityDescription(
            key="hc2_name",
            name="HC2 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc2_on",
            name="HC2",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc2_cooling",
            name="HC2 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc2_circulation_valve",
            name="HC2 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc2_water_requested",
            name="HC2 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc2_water_temp",
            name="HC2 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc2_auto",
            name="HC2 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc2_ambient_requested",
            name="HC2 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc2_ambient_temp",
            name="HC2 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc2.ambient_requested",
            name="HC2 Thermostat",
            current_temperature_path="heating_circuits.hc2.ambient_temp",
            requested_temperature_path="heating_circuits.hc2.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc2_pad_current_humidity",
                name="HC2 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc3": {
        "name": MasterthermSensorEntityDescription(
            key="hc3_name",
            name="HC3 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc3_on",
            name="HC3",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc3_cooling",
            name="HC3 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc3_circulation_valve",
            name="HC3 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc3_water_requested",
            name="HC3 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc3_water_temp",
            name="HC3 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc3_auto",
            name="HC3 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc3_ambient_requested",
            name="HC3 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc3_ambient_temp",
            name="HC3 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc3.ambient_requested",
            name="HC3 Thermostat",
            current_temperature_path="heating_circuits.hc3.ambient_temp",
            requested_temperature_path="heating_circuits.hc3.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc3_pad_current_humidity",
                name="HC3 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc4": {
        "name": MasterthermSensorEntityDescription(
            key="hc4_name",
            name="HC4 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc4_on",
            name="HC4",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc4_cooling",
            name="HC4 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc4_circulation_valve",
            name="HC4 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc4_water_requested",
            name="HC4 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc4_water_temp",
            name="HC4 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc4_auto",
            name="HC4 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc4_ambient_requested",
            name="HC4 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc4_ambient_temp",
            name="HC4 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc4.ambient_requested",
            name="HC4 Thermostat",
            current_temperature_path="heating_circuits.hc4.ambient_temp",
            requested_temperature_path="heating_circuits.hc4.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc4_pad_current_humidity",
                name="HC4 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc5": {
        "name": MasterthermSensorEntityDescription(
            key="hc5_name",
            name="HC5 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc5_on",
            name="HC5",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc5_cooling",
            name="HC5 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc5_circulation_valve",
            name="HC5 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc5_water_requested",
            name="HC5 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc5_water_temp",
            name="HC5 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc5_auto",
            name="HC5 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc5_ambient_requested",
            name="HC5 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc5_ambient_temp",
            name="HC5 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc5.ambient_requested",
            name="HC5 Thermostat",
            current_temperature_path="heating_circuits.hc5.ambient_temp",
            requested_temperature_path="heating_circuits.hc5.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc5_pad_current_humidity",
                name="HC5 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "hc6": {
        "name": MasterthermSensorEntityDescription(
            key="hc6_name",
            name="HC6 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc6_on",
            name="HC6",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc6_cooling",
            name="HC6 Cooling",
        ),
        "circulation_valve": MasterthermBinarySensorEntityDescription(
            key="hc6_circulation_valve",
            name="HC6 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "water_requested": MasterthermSensorEntityDescription(
            key="hc6_water_requested",
            name="HC6 Water Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_temp": MasterthermSensorEntityDescription(
            key="hc6_water_temp",
            name="HC6 Water Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc6_auto",
            name="HC6 Auto",
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc6_ambient_requested",
            name="HC6 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc6_ambient_temp",
            name="HC6 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "thermostat": MasterthermClimateEntityDescription(
            key="heating_circuits.hc6.ambient_requested",
            name="HC6 Thermostat",
            current_temperature_path="heating_circuits.hc6.ambient_temp",
            requested_temperature_path="heating_circuits.hc6.ambient_requested",
        ),
        "pad": {
            "current_humidity": MasterthermSensorEntityDescription(
                key="hc6_pad_current_humidity",
                name="HC6 PAD Current Humidity",
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=PERCENTAGE,
                suggested_unit_of_measurement=PERCENTAGE,
            ),
        },
    },
    "solar": {
        "name": MasterthermSensorEntityDescription(
            key="solar_name",
            name="Solar Name",
        ),
        "s1_temp": MasterthermSensorEntityDescription(
            key="solar_s1_temp",
            name="Solar 1 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "s2_temp": MasterthermSensorEntityDescription(
            key="solar_s2_temp",
            name="Solar 2 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "s3_temp": MasterthermSensorEntityDescription(
            key="solar_s3_temp",
            name="Solar 3 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    },
    "pool": {
        "name": MasterthermSensorEntityDescription(
            key="solar_name",
            name="Solar Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="pool_on",
            name="Pool",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
        ),
        "heating": MasterthermBinarySensorEntityDescription(
            key="pool_heating",
            name="Pool Heating",
            device_class=BinarySensorDeviceClass.HEAT,
        ),
        "s1_temp": MasterthermSensorEntityDescription(
            key="pool_s1_temp",
            name="Pool Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "temp_requested": MasterthermSensorEntityDescription(
            key="pool_temp_requested",
            name="Pool Temperature Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    },
}

ENTITY_TYPES_MAP: dict = {
    "hp_power_state": MasterthermSwitchEntityDescription(
        key="hp_power_state",
        name="HP Power",
        device_class=SwitchDeviceClass.SWITCH,
        icon="mdi:power",
    ),
    "hp_function": MasterthermSelectEntityDescription(
        key="hp_function",
        name="HP Function",
        translation_key="hp_function",
        options_map={
            "heating": 0,
            "cooling": 1,
            "auto": 2,
        },
        options=["heating", "cooling", "auto"],
        read_only=True,
    ),
    "season": MasterthermSensorEntityDescription(
        key="season",
        name="Season",
        translation_key="hp_season",
        icon="mdi:weather-partly-snowy-rainy",
        icon_state_map={
            "winter": "mdi:weather-snowy-heavy",
            "summer": "mdi:weather-sunny",
            "auto:winter": "mdi:weather-snowy-heavy",
            "auto:summer": "mdi:weather-sunny",
        },
    ),
    "operating_mode": MasterthermSensorEntityDescription(
        key="operating_mode",
        name="HP Operating Mode",
        icon="mdi:weather-partly-snowy-rainy",
        translation_key="hp_season",
        icon_state_map={
            "heating": "mdi:sun-thermometer",
            "cooling": "mdi:coolant-temperature",
            "pool": "mdi:pool",
            "dhw": "mdi:water-pump",
            "dpc": "mdi:snowflake-melt",
        },
    ),
    "cooling_mode": MasterthermBinarySensorEntityDescription(
        key="cooling_mode",
        name="Cooling Mode",
    ),
    "domestic_hot_water": {
        "heating": MasterthermBinarySensorEntityDescription(
            key="dhw_heating",
            name="DHW Heating",
        ),
        "enabled": MasterthermSensorEntityDescription(
            key="dhw_enabled",
            name="DHW Enabled",
            icon="mdi:thermometer-water",
        ),
        "current_temp": MasterthermSensorEntityDescription(
            key="dhw_current_temp",
            name="DHW Actual Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "required_temp": MasterthermSensorEntityDescription(
            key="dhw_required_temp",
            name="DHW Required Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    },
    "compressor_running": MasterthermBinarySensorEntityDescription(
        key="compressor_running",
        name="Compressor",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    "compressor2_running": MasterthermBinarySensorEntityDescription(
        key="compressor2_running",
        name="Compressor 2",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    "circulation_pump_running": MasterthermBinarySensorEntityDescription(
        key="circulation_pump_running",
        name="Circulation Pump",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    "fan_running": MasterthermBinarySensorEntityDescription(
        key="fan_running",
        name="Fan",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    "defrost_mode": MasterthermBinarySensorEntityDescription(
        key="defrost_mode",
        name="Defrost Mode",
    ),
    "aux_heater_1": MasterthermBinarySensorEntityDescription(
        key="aux_heater_1",
        name="Aux Heater 1",
    ),
    "aux_heater_2": MasterthermBinarySensorEntityDescription(
        key="aux_heater_2",
        name="Aux Heater 2",
    ),
    "outside_temp": MasterthermSensorEntityDescription(
        key="outside_temp",
        name="Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "requested_temp": MasterthermSensorEntityDescription(
        key="requested_temp",
        name="HP Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "actual_temp": MasterthermSensorEntityDescription(
        key="actual_temp",
        name="HP Actual Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "dewp_control": MasterthermBinarySensorEntityDescription(
        key="dewp_control",
        name="Dew Point Control",
    ),
    "hdo_on": MasterthermBinarySensorEntityDescription(
        key="hdo_on",
        name="High Tarrif (HDO)",
    ),
    "runtime_info": {
        "compressor_run_time": MasterthermSensorEntityDescription(
            key="compressor_run_time",
            name="Compressor Runtime",
            icon="mdi:progress-clock",
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=TIME_HOURS,
            suggested_unit_of_measurement=TIME_HOURS,
        ),
        "compressor_start_counter": MasterthermSensorEntityDescription(
            key="compressor_start_counter",
            name="Compressor Start Counter",
            icon="mdi:timer",
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        "pump_runtime": MasterthermSensorEntityDescription(
            key="pump_runtime",
            name="Pump Runtime",
            icon="mdi:progress-clock",
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=TIME_HOURS,
            suggested_unit_of_measurement=TIME_HOURS,
        ),
        "aux1_runtime": MasterthermSensorEntityDescription(
            key="aux1_runtime",
            name="Aux 1 Runtime",
            icon="mdi:progress-clock",
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=TIME_HOURS,
            suggested_unit_of_measurement=TIME_HOURS,
        ),
        "aux2_runtime": MasterthermSensorEntityDescription(
            key="aux2_runtime",
            name="Aux 2 Runtime",
            icon="mdi:progress-clock",
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=TIME_HOURS,
            suggested_unit_of_measurement=TIME_HOURS,
        ),
    },
    "season_info": {
        "hp_season": MasterthermSwitchEntityDescription(
            key="winter_season",
            name="Winter Season",
            device_class=SwitchDeviceClass.SWITCH,
            read_only=True,
        ),
        "hp_seasonset": MasterthermSwitchEntityDescription(
            key="auto_season",
            name="Auto Season",
            device_class=SwitchDeviceClass.SWITCH,
            read_only=True,
        ),
    },
    "error_info": {
        "some_error": MasterthermBinarySensorEntityDescription(
            key="somer_error",
            name="Some Error",
        ),
        "three_errors": MasterthermBinarySensorEntityDescription(
            key="three_errors",
            name="Three Errors",
        ),
        "reset_3e": MasterthermBinarySensorEntityDescription(
            key="reset_3e",
            name="Reset 3E",
        ),
        "safety_tstat": MasterthermBinarySensorEntityDescription(
            key="safety_tstat",
            name="Reset 3E",
        ),
    },
    "heating_circuits": HEATING_CIRCUITS,
}

"""Contains all the Entity Mappings from the Mastertherm Connector"""
from dataclasses import dataclass, field

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
from homeassistant.const import Platform
from homeassistant.helpers.entity import EntityDescription


@dataclass
class MasterthermBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Description for the Mastertherm binary sensor entities."""


@dataclass
class MasterthermSelectEntityDescription(SelectEntityDescription):
    """Description for the Mastertherm select entities."""

    options_map: dict = field(default_factory=dict)
    read_only: bool = False


@dataclass
class MasterthermSensorEntityDescription(SensorEntityDescription):
    """Description for the Mastertherm sensor entities."""


@dataclass
class MasterthermSwitchEntityDescription(SwitchEntityDescription):
    """Description for the Mastertherm switch entities."""

    read_only: bool = False


ENTITIES: dict[str, str] = {
    MasterthermBinarySensorEntityDescription.__name__: Platform.BINARY_SENSOR,
    MasterthermSelectEntityDescription.__name__: Platform.SELECT,
    MasterthermSensorEntityDescription.__name__: Platform.SENSOR,
    MasterthermSwitchEntityDescription.__name__: Platform.SWITCH,
}

# Putting all entities into a single map which hopfully makes it easier
# to maintain, will split into usable entity lists in the coordinator.
HEATING_CIRCUITS: dict = {
    "hc0": {
        "name": MasterthermSensorEntityDescription(
            key="hc0_name",
            name="HC0 Name",
        ),
        "on": MasterthermSwitchEntityDescription(
            key="hc0_on",
            name="HC0",
            device_class=SwitchDeviceClass.SWITCH,
            icon="mdi:power",
            read_only=True,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc0_ambient_temp",
            name="HC0 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc0_ambient_requested",
            name="HC0 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "pad": {
            "active": MasterthermBinarySensorEntityDescription(
                key="hc0_pad_active",
                name="HC0 PAD Active",
            ),
            "enabled": MasterthermBinarySensorEntityDescription(
                key="hc0_pad_enabled",
                name="HC0 PAD Enabled",
            ),
            "temp": MasterthermSensorEntityDescription(
                key="hc0_pad_temp",
                name="HC0 PAD Temperature",
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
            ),
            "temp_requested": MasterthermSensorEntityDescription(
                key="hc0_pad_temp_requested",
                name="HC0 PAD Requested Temperature",
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc1_cooling",
            name="HC1 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc1_pump_running",
            name="HC1 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc1_ambient_temp",
            name="HC1 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc1_ambient_requested",
            name="HC1 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc1_auto",
            name="HC1 Auto",
        ),
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc2_cooling",
            name="HC2 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc2_pump_running",
            name="HC2 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc2_ambient_temp",
            name="HC2 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc2_ambient_requested",
            name="HC2 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc2_auto",
            name="HC2 Auto",
        ),
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc3_cooling",
            name="HC3 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc3_pump_running",
            name="HC3 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc3_ambient_temp",
            name="HC3 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc3_ambient_requested",
            name="HC3 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc3_auto",
            name="HC3 Auto",
        ),
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc4_cooling",
            name="HC4 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc4_pump_running",
            name="HC4 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc4_ambient_temp",
            name="HC4 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc4_ambient_requested",
            name="HC4 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc4_auto",
            name="HC4 Auto",
        ),
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc5_cooling",
            name="HC5 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc5_pump_running",
            name="HC5 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc5_ambient_temp",
            name="HC5 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc5_ambient_requested",
            name="HC5 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc5_auto",
            name="HC5 Auto",
        ),
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
            read_only=True,
        ),
        "cooling": MasterthermBinarySensorEntityDescription(
            key="hc6_cooling",
            name="HC6 Cooling",
        ),
        "pump_running": MasterthermBinarySensorEntityDescription(
            key="hc6_pump_running",
            name="HC6 Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc6_ambient_temp",
            name="HC6 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "ambient_requested": MasterthermSensorEntityDescription(
            key="hc6_ambient_requested",
            name="HC6 Ambient Requested",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "auto": MasterthermSensorEntityDescription(
            key="hc6_auto",
            name="HC6 Auto",
        ),
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
            read_only=True,
        ),
        "heating": MasterthermBinarySensorEntityDescription(
            key="pool_heating",
            name="Pool Circulation Valve",
            device_class=BinarySensorDeviceClass.OPENING,
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
        read_only=True,
    ),
    "hp_function": MasterthermSelectEntityDescription(
        key="hp_function",
        name="HP Function",
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
        icon="mdi:weather-partly-snowy-rainy",
    ),
    "operating_mode": MasterthermSensorEntityDescription(
        key="operating_mode",
        name="HP Operating Mode",
        icon="mdi:weather-partly-snowy-rainy",
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
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        "compressor_start_counter": MasterthermSensorEntityDescription(
            key="compressor_start_counter",
            name="Compressor Start Counter",
            icon="mdi:count",
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        "pump_runtime": MasterthermSensorEntityDescription(
            key="pump_runtime",
            name="Pump Runtime",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        "aux1_runtime": MasterthermSensorEntityDescription(
            key="aux1_runtime",
            name="Aux 1 Runtime",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        "aux2_runtime": MasterthermSensorEntityDescription(
            key="aux2_runtime",
            name="Aux 2 Runtime",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.TOTAL_INCREASING,
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

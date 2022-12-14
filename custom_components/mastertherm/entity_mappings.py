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
from homeassistant.helpers.entity import EntityDescription


@dataclass
class MasterthermSwitchEntityDescription(SwitchEntityDescription):
    """Description for the Mastertherm switch entities."""


@dataclass
class MasterthermSelectEntityDescription(SelectEntityDescription):
    """Description for the Mastertherm select entities."""

    options_map: dict = field(default_factory=dict)


@dataclass
class MasterthermSensorEntityDescription(SensorEntityDescription):
    """Description for the Mastertherm sensor entities."""


@dataclass
class MasterthermBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Description for the Mastertherm binary sensor entities."""


SWITCH_TYPES: dict[str, MasterthermSwitchEntityDescription] = {
    "hp_power_state": MasterthermSwitchEntityDescription(
        key="hp_power_state",
        name="HP Power",
        device_class=SwitchDeviceClass.SWITCH,
        icon="mdi:power",
    ),
    "domestic_hot_water.enabled": MasterthermSwitchEntityDescription(
        key="dhw_enabled",
        name="DHW Enabled",
        device_class=SwitchDeviceClass.SWITCH,
        icon="mdi:thermometer-water",
    ),
}

# Disabled for Now
SELECT_TYPES: dict[str, MasterthermSelectEntityDescription] = {
    "hp_function": MasterthermSelectEntityDescription(
        key="hp_function",
        name="HP Function",
        options_map={
            "Heating": 0,
            "Cooling": 1,
            "Auto": 2,
        },
        options=["heating", "cooling", "auto"],
    ),
}

SENSOR_TYPES: dict[str, MasterthermSensorEntityDescription] = {
    "season": MasterthermSensorEntityDescription(
        key="season",
        name="Season",
        icon="mdi:weather-partly-snowy-rainy",
    ),
    "operating_mode": MasterthermSensorEntityDescription(
        key="operating_mode",
        name="HP Operating Mode",
        icon="mdi:sun-thermomete",
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
    "domestic_hot_water.current_temp": MasterthermSensorEntityDescription(
        key="dhw_current_temp",
        name="DHW Actual Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "domestic_hot_water.required_temp": MasterthermSensorEntityDescription(
        key="dhw_required_temp",
        name="DHW Required Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "runtime_info.compressor_run_time": MasterthermSensorEntityDescription(
        key="compressor_run_time",
        name="Compressor Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "runtime_info.compressor_start_counter": MasterthermSensorEntityDescription(
        key="compressor_start_counter",
        name="Compressor Start Counter",
        icon="mdi:count",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "runtime_info.pump_runtime": MasterthermSensorEntityDescription(
        key="pump_runtime",
        name="Pump Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "runtime_info.aux1_runtime": MasterthermSensorEntityDescription(
        key="aux1_runtime",
        name="Aux 1 Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "runtime_info.aux2_runtime": MasterthermSensorEntityDescription(
        key="aux2_runtime",
        name="Aux 2 Runtime",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "heating_circuits.hc0.name": MasterthermSensorEntityDescription(
        key="hc0_name",
        name="HC0 Name",
    ),
    "heating_circuits.hc0.ambient_temp": MasterthermSensorEntityDescription(
        key="hc0_ambient_temp",
        name="HC0 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc0.ambient_requested": MasterthermSensorEntityDescription(
        key="hc0_ambient_requested",
        name="HC0 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc0.pad.temp": MasterthermSensorEntityDescription(
        key="hc0_pad_temp",
        name="HC0 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc0.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc0_pad_temp_requested",
        name="HC0 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc1.name": MasterthermSensorEntityDescription(
        key="hc1_name",
        name="HC1 Name",
    ),
    "heating_circuits.hc1.ambient_temp": MasterthermSensorEntityDescription(
        key="hc1_ambient_temp",
        name="HC1 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc1.ambient_requested": MasterthermSensorEntityDescription(
        key="hc1_ambient_requested",
        name="HC1 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc1.pad.temp": MasterthermSensorEntityDescription(
        key="hc1_pad_temp",
        name="HC1 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc1.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc1_pad_temp_requested",
        name="HC1 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc2.name": MasterthermSensorEntityDescription(
        key="hc2_name",
        name="HC2 Name",
    ),
    "heating_circuits.hc2.ambient_temp": MasterthermSensorEntityDescription(
        key="hc2_ambient_temp",
        name="HC2 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc2.ambient_requested": MasterthermSensorEntityDescription(
        key="hc2_ambient_requested",
        name="HC2 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc2.pad.temp": MasterthermSensorEntityDescription(
        key="hc2_pad_temp",
        name="HC2 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc2.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc2_pad_temp_requested",
        name="HC2 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc3.name": MasterthermSensorEntityDescription(
        key="hc3_name",
        name="HC3 Name",
    ),
    "heating_circuits.hc3.ambient_temp": MasterthermSensorEntityDescription(
        key="hc3_ambient_temp",
        name="HC3 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc3.ambient_requested": MasterthermSensorEntityDescription(
        key="hc3_ambient_requested",
        name="HC3 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc3.pad.temp": MasterthermSensorEntityDescription(
        key="hc3_pad_temp",
        name="HC3 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc3.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc3_pad_temp_requested",
        name="HC3 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc4.name": MasterthermSensorEntityDescription(
        key="hc4_name",
        name="HC4 Name",
    ),
    "heating_circuits.hc4.ambient_temp": MasterthermSensorEntityDescription(
        key="hc4_ambient_temp",
        name="HC4 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc4.ambient_requested": MasterthermSensorEntityDescription(
        key="hc4_ambient_requested",
        name="HC4 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc4.pad.temp": MasterthermSensorEntityDescription(
        key="hc4_pad_temp",
        name="HC4 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc4.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc4_pad_temp_requested",
        name="HC4 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc5.name": MasterthermSensorEntityDescription(
        key="hc5_name",
        name="HC5 Name",
    ),
    "heating_circuits.hc5.ambient_temp": MasterthermSensorEntityDescription(
        key="hc5_ambient_temp",
        name="HC5 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc5.ambient_requested": MasterthermSensorEntityDescription(
        key="hc5_ambient_requested",
        name="HC5 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc5.pad.temp": MasterthermSensorEntityDescription(
        key="hc5_pad_temp",
        name="HC5 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc5.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc5_pad_temp_requested",
        name="HC5 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc6.name": MasterthermSensorEntityDescription(
        key="hc6_name",
        name="HC6 Name",
    ),
    "heating_circuits.hc6.ambient_temp": MasterthermSensorEntityDescription(
        key="hc6_ambient_temp",
        name="HC6 Ambient Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc6.ambient_requested": MasterthermSensorEntityDescription(
        key="hc6_ambient_requested",
        name="HC6 Ambient Requested",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc6.pad.temp": MasterthermSensorEntityDescription(
        key="hc6_pad_temp",
        name="HC6 PAD Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "heating_circuits.hc6.pad.temp_requested": MasterthermSensorEntityDescription(
        key="hc6_pad_temp_requested",
        name="HC6 PAD Requested Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
}

BINARY_SENSOR_TYPES: dict[str, MasterthermBinarySensorEntityDescription] = {
    "cooling_mode": MasterthermBinarySensorEntityDescription(
        key="cooling_mode",
        name="Cooling Mode",
    ),
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
    "dewp_control": MasterthermBinarySensorEntityDescription(
        key="dewp_control",
        name="Dew Point Control",
    ),
    "hdo_on": MasterthermBinarySensorEntityDescription(
        key="hdo_on",
        name="High Tarrif (HDO)",
    ),
    "domestic_hot_water.heating": MasterthermBinarySensorEntityDescription(
        key="dwh_heating",
        name="DHW Heating",
    ),
    "season.hp_season": MasterthermBinarySensorEntityDescription(
        key="winter_season",
        name="Winter Season",
    ),
    "error_info.some_error": MasterthermBinarySensorEntityDescription(
        key="somer_error",
        name="Some Error",
    ),
    "error_info.three_errors": MasterthermBinarySensorEntityDescription(
        key="three_errors",
        name="Three Errors",
    ),
    "error_info.reset_3e": MasterthermBinarySensorEntityDescription(
        key="reset_3e",
        name="Reset 3E",
    ),
    "error_info.safety_tstat": MasterthermBinarySensorEntityDescription(
        key="safety_tstat",
        name="Reset 3E",
    ),
    "heating_circuits.hc0.on": MasterthermBinarySensorEntityDescription(
        key="hc9_on",
        name="HC0 Heating",
    ),
    "heating_circuits.hc0.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc9_pad_enabled",
        name="HC0 PAD Enabled",
    ),
    "heating_circuits.hc1.on": MasterthermBinarySensorEntityDescription(
        key="hc1_on",
        name="HC1 Heating",
    ),
    "heating_circuits.hc1.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc1_pad_enabled",
        name="HC1 PAD Enabled",
    ),
    "heating_circuits.hc2.on": MasterthermBinarySensorEntityDescription(
        key="hc2_on",
        name="HC2 Heating",
    ),
    "heating_circuits.hc2.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc2_pad_enabled",
        name="HC2 PAD Enabled",
    ),
    "heating_circuits.hc3.on": MasterthermBinarySensorEntityDescription(
        key="hc3_on",
        name="HC3 Heating",
    ),
    "heating_circuits.hc3.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc3_pad_enabled",
        name="HC3 PAD Enabled",
    ),
    "heating_circuits.hc4.on": MasterthermBinarySensorEntityDescription(
        key="hc4_on",
        name="HC4 Heating",
    ),
    "heating_circuits.hc4.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc4_pad_enabled",
        name="HC4 PAD Enabled",
    ),
    "heating_circuits.hc5.on": MasterthermBinarySensorEntityDescription(
        key="hc5_on",
        name="HC5 Heating",
    ),
    "heating_circuits.hc5.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc5_pad_enabled",
        name="HC5 PAD Enabled",
    ),
    "heating_circuits.hc6.on": MasterthermBinarySensorEntityDescription(
        key="hc6_on",
        name="HC6 Heating",
    ),
    "heating_circuits.hc6.pad.enabled": MasterthermBinarySensorEntityDescription(
        key="hc6_pad_enabled",
        name="HC6 PAD Enabled",
    ),
}

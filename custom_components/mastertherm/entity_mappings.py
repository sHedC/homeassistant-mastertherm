"""Contains all the Entity Mappings from the Mastertherm Connector"""
from dataclasses import dataclass

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


@dataclass
class MasterthermSwitchEntityDescription(SwitchEntityDescription):
    """Description for the Mastertherm switch entities."""


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
}

SENSOR_TYPES: dict[str, MasterthermSensorEntityDescription] = {
    "hp_function": MasterthermSensorEntityDescription(
        key="hp_function",
        name="HP Function",
    ),
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
}

BINARY_SENSOR_TYPES: dict[str, MasterthermBinarySensorEntityDescription] = {
    "hp_power_state": MasterthermBinarySensorEntityDescription(
        key="hp_power_state",
        name="Heatpump Power",
        device_class=BinarySensorDeviceClass.POWER,
    ),
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
}

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
        name="Heatpump Power",
        device_class=SwitchDeviceClass.SWITCH,
        icon="mdi:power",
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
        name="Operating Mode",
        icon="mdi:sun-thermomete",
    ),
    "outside_temp": MasterthermSensorEntityDescription(
        key="outside_temp",
        name="Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
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
}

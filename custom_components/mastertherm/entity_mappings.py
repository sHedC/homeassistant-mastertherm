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
from homeassistant.components.switch import SwitchEntityDescription, DEVICE_CLASS_SWITCH


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
        key="heatpump_power",
        name="Heatpump Power",
        device_class=DEVICE_CLASS_SWITCH,
        icon="mdi:power",
    )
}

SENSOR_TYPES: dict[str, MasterthermSensorEntityDescription] = {
    "outside_temp": MasterthermSensorEntityDescription(
        key="outside_temp",
        name="Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    )
}

BINARY_SENSOR_TYPES: dict[str, MasterthermBinarySensorEntityDescription] = {
    "hp_power_state": MasterthermBinarySensorEntityDescription(
        key="hp_power_state",
        name="Heatpump Power State",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    "compressor_running": MasterthermBinarySensorEntityDescription(
        key="compressor_running",
        name="Compressor Running",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
}

"""Contains all the Entity Mappings from the Mastertherm Connector"""
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import PERCENTAGE, TIME_HOURS, UnitOfTemperature

from .const import (
    MasterthermBinarySensorEntityDescription,
    MasterthermClimateEntityDescription,
    MasterthermNumberEntityDescription,
    MasterthermSelectEntityDescription,
    MasterthermSensorEntityDescription,
    MasterthermSwitchEntityDescription,
)

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
        "ambient_temp": MasterthermSensorEntityDescription(
            key="hc1_ambient_temp",
            name="HC1 Ambient Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC1 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC1 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC1 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC1 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC1 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC1 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC1 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC1 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC1 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC1 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC1 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC1 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC1 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC1 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC1 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC1 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC3 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC3 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC3 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC3 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC3 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC3 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC3 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC3 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC4 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC4 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC4 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC4 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC4 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC4 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC4 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC4 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC5 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC5 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC5 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC5 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC5 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC5 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC5 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC5 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
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
        "control_curve_heating": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_outside",
                name="HC6 Heating Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_a_requested",
                name="HC6 Heating Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_outside",
                name="HC6 Heating Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_heating.setpoint_b_requested",
                name="HC6 Heating Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
        "control_curve_cooling": {
            "setpoint_a_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_outside",
                name="HC6 Cooling Curve A Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_a_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_a_requested",
                name="HC6 Cooling Curve A Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
            "setpoint_b_outside": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_outside",
                name="HC6 Cooling Curve B Outside",
                native_min_value=-30.0,
                native_max_value=30.0,
            ),
            "setpoint_b_requested": MasterthermNumberEntityDescription(
                key="control_curve_cooling.setpoint_b_requested",
                name="HC6 Cooling Curve B Requested",
                native_min_value=20.0,
                native_max_value=50.0,
            ),
        },
    },
    "solar": {
        "name": MasterthermSensorEntityDescription(
            key="solar_name",
            name="Solar Name",
        ),
        "solar_collector": MasterthermSensorEntityDescription(
            key="solar_collector",
            name="Solar 1 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_tank1": MasterthermSensorEntityDescription(
            key="solar_water_tank1",
            name="Solar Water Tank 1 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        "water_tank2": MasterthermSensorEntityDescription(
            key="solar_water_tank2",
            name="Solar Water Tank 2 Temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    },
    "pool": {
        "name": MasterthermSensorEntityDescription(
            key="pool_name",
            name="Pool Name",
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
        "temp_actual": MasterthermSensorEntityDescription(
            key="pool_temp_actual",
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
        "control": MasterthermClimateEntityDescription(
            key="heating_circuits.pool.enabled",
            name="Pool Control",
            current_temperature_path="heating_circuits.pool.temp_actual",
            requested_temperature_path="heating_circuits.pool.temp_requested",
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
    ),
    "season": {
        "mode": MasterthermSensorEntityDescription(
            key="season_mode",
            name="Season",
            translation_key="hp_season",
            icon="mdi:weather-partly-snowy-rainy",
            icon_state_map={
                "winter": "mdi:weather-snowy-heavy",
                "summer": "mdi:weather-sunny",
                "auto-winter": "mdi:weather-snowy-heavy",
                "auto-summer": "mdi:weather-sunny",
            },
        ),
        "select": MasterthermSelectEntityDescription(  # ID is hard codes.
            key="season_select",
            name="Season Select",
            translation_key="season_select",
            options=["auto", "winter", "summer"],
        ),
        "winter_temp": MasterthermNumberEntityDescription(
            key="winter_temp",
            name="Winter Temperature",
            native_min_value=-20.0,
            native_max_value=40.0,
        ),
        "summer_temp": MasterthermNumberEntityDescription(
            key="summer_temp",
            name="Summer Temperature",
            native_min_value=-20.0,
            native_max_value=40.0,
        ),
    },
    "operating_mode": MasterthermSensorEntityDescription(
        key="operating_mode",
        name="HP Operating Mode",
        icon="mdi:weather-partly-snowy-rainy",
        translation_key="hp_operating_mode",
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
    "control_curve_heating": {
        "setpoint_a_outside": MasterthermNumberEntityDescription(
            key="control_curve_heating.setpoint_a_outside",
            name="Heating Curve A Outside",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=-30.0,
            native_max_value=30.0,
        ),
        "setpoint_a_requested": MasterthermNumberEntityDescription(
            key="control_curve_heating.setpoint_a_requested",
            name="Heating Curve A Requested",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=20.0,
            native_max_value=50.0,
        ),
        "setpoint_b_outside": MasterthermNumberEntityDescription(
            key="control_curve_heating.setpoint_b_outside",
            name="Heating Curve B Outside",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=-30.0,
            native_max_value=30.0,
        ),
        "setpoint_b_requested": MasterthermNumberEntityDescription(
            key="control_curve_heating.setpoint_b_requested",
            name="Heating Curve B Requested",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=20.0,
            native_max_value=50.0,
        ),
    },
    "control_curve_cooling": {
        "setpoint_a_outside": MasterthermNumberEntityDescription(
            key="control_curve_cooling.setpoint_a_outside",
            name="Cooling Curve A Outside",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=-30.0,
            native_max_value=30.0,
        ),
        "setpoint_a_requested": MasterthermNumberEntityDescription(
            key="control_curve_cooling.setpoint_a_requested",
            name="Cooling Curve A Requested",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=20.0,
            native_max_value=50.0,
        ),
        "setpoint_b_outside": MasterthermNumberEntityDescription(
            key="control_curve_cooling.setpoint_b_outside",
            name="Cooling Curve B Outside",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=-30.0,
            native_max_value=30.0,
        ),
        "setpoint_b_requested": MasterthermNumberEntityDescription(
            key="control_curve_cooling.setpoint_b_requested",
            name="Cooling Curve B Requested",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            native_min_value=20.0,
            native_max_value=50.0,
        ),
    },
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
        "control": MasterthermClimateEntityDescription(
            key="domestic_hot_water.enabled",
            name="DHW Control",
            min_temp="domestic_hot_water.min_temp",
            max_temp="domestic_hot_water.max_temp",
            current_temperature_path="domestic_hot_water.current_temp",
            requested_temperature_path="domestic_hot_water.required_temp",
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

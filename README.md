# Mastertherm
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Stable -
[![GitHub Release][stable-release-shield]][releases]
[![workflow-release]][workflows-release]
[![codecov][codecov-shield]][codecov-link]

Latest -
[![GitHub Release][latest-release-shield]][releases]
[![workflow-lastest]][workflows]
[![issues][issues-shield]][issues-link]

## Please Read
My friend who helps a lot with debugging and identifying details for this integration broke his system during this process and had to pay a couple of hundred Euros for it to be re-initialised. If you would like to support him to recover some of this please buy him a coffee.

SeBsZ Link: [![BuyMeCoffee][buymecoffeebadge_sebs]][buymecoffee_sebs]

## About the Integration
![mastertherm][masterthermimg]

An integration for homeassistant (via HACS) to connect to Mastertherm Heat Pumps, Air Source/ Ground Source and Water Source. There are two entry points for the Mastertherm Heat Pumps:
- mastertherm.vip-it.cz - This is the server for pre 2022 heat pumps
- mastertherm.online - This is the server for 2022 onward

NOTES:
- The systems do not like multiple requests at the same time from the same IP and this leads to Server Disconnect messages, so using the App and this integration it could cause intermittent disconnects.
- The integration restricts requests to one request every 0.2 seconds to avoid intermittent errors, this means if you trigger 10 updates at the same time it will take 2 seconds to complete the updates to the Heat Pump.
- Mastertherm.Online is sensitive to too many login attempts and requests, to avoid issues the minimum update time is 30 seconds and pump information is updated every 30 minutes. Additionally the integration will only attempt to re-login if the token expires or becomes invalid.  It reports on other types of temporary issues but does not try to re-log in until those issues stop e.g. API is unavailable.

Mastertherm only allows a single install, mutliple accounts are not currently supported.  Additionally if you have an installation with more than 2 units/ devices keep the refresh rate as at least 2 min or even increase it, the app/ web only connects to a single device/ unit at a time and refreshes every 30 seconds but this integration retrieves all device and unit combinations.

Local connection is not possible at this time, it seems the heat pumps connect to the servers using SSH.

## Installation
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS.

Go to HACS and integraitons, then select to download Mastertherm from HACS.

## Configuration
Go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

Two additonal options are given, as most updates are delta updates sometimes the Web API does not report a change, probably because of timeing issues.  These settings are used to avoid that.
- Minutes between full data refresh - this tells the coordinator to do a full data refresh every x minutes
- Offset last data update time - this tells a delta update to look back in time from when the Web API reports the last update

<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/login.jpg?raw=true" width="50%" height="50%">
<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/options.jpg?raw=true" width="50%" height="50%">

#### Beta Versions
If you want to see Beta versions open the Mastertherm in HACS, after download, and click the three dots on the top right and select re-download. Here you will se an option to see beta versions.

#### Debugging
It is possible to show the info and debug logs for the mastertherm integration and mastertherm connect, to do this you need to enable logging in the configuration.yaml, example below:

Logs do not remove sensitive information so careful what you share, you should always remove the module number replace with xxxx.

```
logger:
  default: warning
  logs:
    # Log for Mastertherm
    custom_components.mastertherm: info
    masterthermconnect: info
```

#### Manual Install
To install manually, if you really want to: I won't support this.
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `mastertherm`.
4. Download _all_ the files from the `custom_components/mastertherm/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add the masterthermconnect module: pip install -I masterthermconnect==2.0.0
7. Restart Home Assistant
8. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"

## Example HASS View
Example View, I don't have thermostats so they are not shown here:
<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/dashboard.jpg?raw=true">

## Automation
To set Thermostats such as requested temperature use the Call Service: Climate feature.

For Automation when looking for conditions some of the states are translated so for a condition what is on the screen is not what should be used in the automation:

Translations are as follows, example for hp_operating_mode shows in the UI "Pump Offline" but for automations its "offline"

```
"select": {
    "hp_function": {
        "state": {
            "auto": "Auto",
            "heating": "Heating",
            "cooling": "Cooling"
        }
    },
    "season_select": {
        "state": {
            "auto": "Auto",
            "winter": "Winter",
            "summer": "Summer"
        }
    }
},
"sensor": {
    "hp_type": {
        "state": {
            "0": "Air Source",
            "1": "Ground Source",
            "2": "Water Source",
            "3": "DX Ground Source",
            "4": "Air Source R",
            "5": "Ground Source R",
            "6": "Water Source R"
        }
    },
    "hp_season": {
        "state": {
            "winter": "Winter",
            "summer": "Summer",
            "auto-winter": "Winter (Auto)",
            "auto-summer": "Summer (Auto)"
        }
    },
    "hp_operating_mode": {
        "state": {
            "offline": "Pump Offline",
            "heating": "Heating",
            "cooling": "Cooling",
            "cooling_dpc": "Cooling (DPC)",
            "pool": "Pool",
            "dhw": "Hot Water",
            "idle": "Idle",
            "aux_heater": "Aux Heater"
        }
    }
}
```

## Sensor Details
What is avaialbe in the app should be available here plus some extras.  There are controls in place to set the min and max values based on what is configured in your heatpump, in addition some features show or are hidden based on your setup, for example if cooling is not installed or disabled it is not shown in Home Assistant.

> :warning: **Heat Pump Configuration Changes:** Changing the configuration of the pump should only be done under the advise of your installer, the changes avaialable to home assistant are based only on the APP UI and some additional from the Thermostats if installed.

A lot of the temperature and modifiable settings have limits that come from the Heatpump, if you want to change these you should speak to your installer.

#### Main Circuit
This section covers entities that are linked tot he Main Heatpump, not all sensors will show up in your configuration depending on your installed configuration.

| Entity | Type | Description |
| ------ | ---- | ----------- |
| hp_power_state | Switch | Turn on and off the Heat Pump |
| hp_function | Select | The function is heating/ cooling or auto |
| operating_mode | Sensor | The current Operating Mode which shows different states: <br/>- Unavailable: The Mastertherm API is uavailable.<br/>- Pump Offline: The HP is offline or unavailable.<br/>- Idle: HP is doing nothing.<br/>- Heating: HP is Heating.<br/>- Cooling: HP is Cooling.<br/>- Cooling (DPC): HP is Cooling with Dew Point Protection.<br/>- Pool: HP is heating the Pool.<br/>- Hot Water: HP is heating domestic hot water.<br/>- Aux Heater: Aux Heater is being used. |
| cooling_mode | Binary Sensor | Whether the pump is in cooling mode or not (if not its heating) |
| compressor_running | Binary Sensor | Main compressor running |
| compressor2_running | Binary Sensor | Compressor 2 if installed |
| circulation_pump_running | Binary Sensor | Circulating water to where it is being requested, this is always true if any circuit is requesting heating or cooling |
| fan_running | Binary Sensor | Ground Source - This is the Brine Pump<br/>Air Source - This is the Fan<br/>Water Source - This is the Water Pump |
| defrost_mode | Binary Sensor | If the heat pump is in defrost mode |
| aux_heater_1 | Binary Sensor | If installed indicates if the auxillary heater is on |
| aux_heater_2 | Binary Sensor | If installed indicates if the second auxillary heater is on |
| outside_temp | Sensor | The outside temperature |
| requested_temp | Sensor | This is the temperature that the heat pump is requesting, it is calcuated by an unknown algorithm and can go higher than expected. An example here is when heating is initially requested it goes higher than needed then reduces as room temperature is reached. |
| actual_temp | Sensor | The actual temperature that the heat pump is up to. |
| dewp_control | Binary Sensor | If Dew Point Control is active |
| high_tariff_control | Binary Sensor | If the feature is enabled then this will show enabled if the system recognized high tariff.  This feature (called HDO_ON) is actually a remote on/off for features on your heatpump that use high energy such as the compressor/ aux heaters and sanitary hot water feature.  It does not disable the DHW function, which also uses the compressor. This feature is really only of use where your have variying high/ low tariff during the day and night or extended periods of low tariff as it disabled heating. |

#### Season Info
| Entity | Type | Description |
| ------ | ---- | ----------- |
| mode | Sensor | The Season mode the heatpump is running on, winter/ summer/ auto winter or auto summer. |
| select | Select | Ability to select the mode, Auto, Winter or Summer |
| winter_temp | Number | The temperature below which is considered winter |
| summer_temp | Number | The temperature above which is considered winter |

#### Control Curves Heating/ Cooling
These are the min and max values to control the heating and cooling curves used by the Heatpump to control the warter temperature.

| Entity | Type | Description |
| ------ | ---- | ----------- |
| setpoint_a_outside | Number | Outside Temperature for Setpoint A, min/ max values are controlled by pump configuration. |
| setpoint_a_requested | Number | Temperature to set for Setpoint A, min/ max values are controlled by pump configuration. |
| setpoint_b_outside | Number | Outside Temperature for Setpoint B, min/ max values are controlled by pump configuration. |
| setpoint_b_requested | Number | Temperature to set for Setpoint B, min/ max values are controlled by pump configuration. |

#### Domestic Hot Water
| Entity | Type | Description |
| ------ | ---- | ----------- |
| heating | Binary Sensor | Whether hot water is requested, also activates if HC1 to 6 is for hot water |
| enabled | Binary Sensor | Not sure on mine always shows disabled. |
| current_temp | Sensor | The current temperature of the hot water, should be taken from the sensor in the water tank |
| required_temp | Sensor | The temperature that was set as required for your hot water, min/ max values are controlled by pump configuration. |
| control | Climate | This is a thermostat allowing control of the requested temperature and to turn on/ off DHW. |

#### Run Time Info
| Entity | Type | Description |
| ------ | ---- | ----------- |
| compressor_run_time | Sensor | Number of hours the compressor has run for |
| compressor_start_counter | Sensor | Probably the number of times the compressor has started |
| pump_runtime | Sensor | The number of hours the circulation pump has run |
| aux1_runtime | Sensor | The house the auxillary heaters have run |
| aux2_runtime | Sensor | The house the auxillary heaters have run |

#### Error Info
| Entity | Type | Description |
| ------ | ---- | ----------- |
| some_errror | BinarySensor | If any Alarm is activated. |
| three_errors | BinarySensor | If three alarms activate, usually requires a pump reset. |
| reset_3e | BinarySensor | Manual Reset required due to three alarms. |
| safety_tstat | BinarySensor | Heater Safety Thermostat Alarm |


#### Heating Circuits
The main circuit is HC0, this is linked to the main pump but some details in this circuit are hidden if any of HC1 to HC6 optional circuits are installed.

HC1 to HC6 are used to provide things like heating/ cooling to different room zones or multiple water tanks for hot water.

HC0 to HC6 may have room thermostat's installed, if used for heating/ cooling, in this case there is a pad sub-section that contains ambient temperatures and humidity.  If not installed then there is an int (internal) sub-section that has the ambient temperatures.

| Entity | Type | Description |
| ------ | ---- | ----------- |
| name | sensor | The name of the circuit, hc0 is usually Home |
| on | Swtich | If the circuit is turns on or not |
| cooling | Binary Sensor | Circuit is in cooling mode |
| circulation_valve | Binary Sensor | If this circuit is requesting then this is open, this also triggers the main circulation pump |
| water_requested | Sensor | The requested water temperature based on heating and cooling curves |
| water_temp | Sensor | The actual water temperature for the circuit |
| auto | Sensor | I believe this controls if the water temperature requested is manually set or automatic based ont he heating/ cooling curves. |
| ambient_temp | Sensor | Ambient temperature, either from the room if the pad is installed or internal |
| ambient_requested | Sensor | requested temperature, either from the room if the pad is installed or internal |
| thermostat | Climate | Allows setting of the room temperature settings. |
| pad.state | Sensor | The Room pad state |
| pad.current_humidity | Sensor | Room Humidity, if the thermostat is installed |
| control_curve_heating | None | Same as the main control curve heating |
| control_curve_cooling | None | Same as the main control curve cooling |

#### Pool and Solar
Solar monitors outside temperature and if enabled can be used to turn on and off the hot water on the heat pump.  Used if you have solar hot water installed.

| Entity | Type | Description |
| ------ | ---- | ----------- |
| name | Sensor | Always Solar |
| solar_collector | Sensor | Temperature of the Solar Panels |
| water_tank1 | Sensor | Temperature of the water in the Hot Water Tank |
| water_tank2 | Sensor | Temperature of the water in Hot Water Tank 2, I believe this can also be Pool temparture. |

Pool monitors and sets the pool temperature.

| Entity | Type | Description |
| ------ | ---- | ----------- |
| name | Sensor | Always Pool |
| on | Switch | If the Pool Controls are on or off |
| heating | BinarySensor | True if the pool is heating |
| temp_actual | Sensor | Actual Temperature of the Pool |
| temp_requested | Sensor | Requested Temperature of the Pool |
| control | Climate | Pool Thermostat |

## Development Envionrment
I have set this up to be able to run development or testing using Visual Studio Code with Docker or Podman in line with the integration blueprint.

To setup just copy the .devcontainer-template.json to .devcontainer.json
- If using podman uncomment the section runArgs to avoid permission issues.
- Update BUILD_TYPE to "run" to run an instance of Home Assistant and "dev" to do development with pytest.

## Contributions are welcome!
If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

Also to determine mappings use the mastertherm connect module directly from the command line where you can get a list of current registers for your heatpump.

Or just raise a feature request, would be useful to have a use-case, what system you have and what you want to get done.

***

[masterthermimg]: https://github.com/sHedC/homeassistant-mastertherm/raw/main/mastertherm.png
[mastertherm]: https://github.com/sHedC/homeassistant-mastertherm
[commits-shield]: https://img.shields.io/github/commit-activity/y/sHedC/homeassistant-mastertherm?style=for-the-badge
[commits]: https://github.com/shedc/homeassistant-mastertherm/commits/main
[license-shield]: https://img.shields.io/github/license/sHedC/homeassistant-mastertherm.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Richard%20Holmes%20%40shedc-blue.svg?style=for-the-badge

[buymecoffee_sebs]: https://www.buymeacoffee.com/sebs89
[buymecoffeebadge_sebs]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat

[buymecoffee]: https://www.buymeacoffee.com/sHedC
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/

[codecov-shield]: https://codecov.io/gh/sHedC/homeassistant-mastertherm/branch/main/graph/badge.svg?token=Z7VVO035GY
[codecov-link]: https://codecov.io/gh/sHedC/homeassistant-mastertherm

[issues-shield]: https://img.shields.io/github/issues/shedc/homeassistant-mastertherm?style=flat
[issues-link]: https://github.com/sHedC/homeassistant-mastertherm/issues

[releases]: https://github.com/shedc/homeassistant-mastertherm/releases
[stable-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-mastertherm?style=flat
[latest-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-mastertherm?include_prereleases&style=flat

[workflows]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/validate.yml/badge.svg
[workflow-lastest]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/validate.yml/badge.svg
[workflows-release]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/release.yml/badge.svg
[workflow-release]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/release.yml/badge.svg

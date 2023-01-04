# Mastertherm
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

Stable -
[![GitHub Release][stable-release-shield]][releases]

Latest -
[![GitHub Release][latest-release-shield]][releases]
[![workflow-lastest]][workflows]


## About
If you feel like donating to a charity, my wife is rasing money for and the Salvation Army here:
<a href="https://www.justgiving.com/fundraising/jackie-holmes1933" target="_blank"><img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/salvationarmy.jpg?raw=true" alt="Charity Link" style="width:125px;height:20px;"></a>

![mastertherm][masterthermimg]

This adds an integration to homeassistant (HACS) to connect to Mastertherm Heat Pumps. There are two entry points for the Mastertherm Heat Pumps:
- mastertherm.vip-it.cz - This is the server for pre 2022 heat pumps
- mastertherm.online - This is the server for 2022 onward

NOTES:
- materhterm.online is sensitive to too many requests, for this reason by default it defaults to updates every 2 minutes, the App updates every 30 seconds. To help the Info updates every 30 min, data can be set in the options down to 30 seconds.
- if multiple requests are sent at the same time (i.e. from home assistant/ the app and web) some will be refused by the servers, its temporary.  The updates have been built to report but ignore these.

## Installation
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS.

At this time its not automatically part of HACS, so after installing HACS, visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-mastertherm.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

Once installed go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct mastertherm login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

Mastertherm only allows a single install, mutliple accounts are not currently supported.  Additionally if you have an installation with more than 2 units/ devices keep the refresh rate as at least 2 min or even increase it, the app/ web only connects to a single device/ unit at a time and refreshes every 30 seconds but this integration retrieves all device and unit combinations.

Local connection is not possible at this time, it seems the heat pumps connect to the servers using SSH.

#### Manual Install
To install manually, if you really want to:
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `mastertherm`.
4. Download _all_ the files from the `custom_components/mastertherm/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add the masterthermconnect module: pip install -I masterthermconnect==1.1.0
7. Restart Home Assistant
8. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"

## Sensor Details
Current version is read only, updates do not work but that will come.

The sensors are based on observations from the Web and Android Applications, the current testing has been done on some basic setup we have not tested options with Solar and Pool but have tried to add sensors based on the apps.
1. One Main circuit with heating and cooling and domestic hot water with attached room thermostats
2. Main Circuit for heating and two optional circuits for Barn and House Domestic Hot Water, no room thermostats

#### Main Circuit
These are the main entities for the heat pump, currently we understand the following.

Entity | Type | Description
-- | -- | --
hp_power_state | Switch | Turn on and off the Heat Pump
hp_function | Select | The function is heating/ cooling or auto
season | Sensor | Shows the Season, Winter or Summer or Auto Winter and Auto Summer
operating_mode | Sensor | The current Operating Mode which shows 5 states: heating/ cooling/ pool/ hot water and defrost protection
cooling_mode | Binary Sensor | Whether the pump is in cooling mode or not (if not its heating)
compressor_running | Binary Sensor | Main compressor running
compressor2_running | Binary Sensor | Compressor 2 if installed
circulation_pump_running | Binary Sensor | Circulating water to where it is being requested, this is always true if any circuit is requesting heating or cooling
fan_running | Binary Sensor | Internal Fan is running
defrost_mode | Binary Sensor | If the heat pump is in defrost mode
aux_heater_1 | Binary Sensor | If installed indicates if the auxillary heater is on
aux_heater_2 | Binary Sensor | If installed indicates if the second auxillary heater is on
outside_temp | Sensor | The outside temperature
requested_temp | Sensor | This is the temperature that the heat pump is requesting, it is calcuated by an unknown algorithm and can go higher than expected. An example here is when heating is initially requested it goes higher than needed then reduces as room temperature is reached.
dewp_control | Binary Sensor | If Dew Point Control is active
hdo_on | Binary Sensor | Something to do with High Tarrif Rates, do not know about this indicator

#### Domestic Hot Water
Entity | Type | Description
-- | -- | --
heating | Binary Sensor | Whether hot water is requested, also activates if HC1 to 6 is for hot water
enabled | Binary Sensor | Not sure on mine always shows disabled.
current_temp | Sensor | The current temperature of the hot water, should be taken from the sensor in the water tank
required_temp | Sensor | The temperature that was set as required for your hot water.

#### Run Time Info
Entity | Type | Description
-- | -- | --
compressor_run_time | Sensor | Number of hours the compressor has run for
compressor_start_counter | Sensor | Probably the number of times the compressor has started
pump_runtime | Sensor | The number of hours the circulation pump has run
aux1_runtime | Sensor | The house the auxillary heaters have run
aux2_runtime | Sensor | The house the auxillary heaters have run

#### Season Info
The switches here define if Winter/ Summer or Auto

Entity | Type | Description
-- | -- | --
hp_season | Switch | If set on then winter, if set off then summer
hp_seasonset | Switch | If set on then Seasion is auto set.

#### Error Info
Work in Progress, error information just decoded from he web application.

Entity | Type | Description
-- | -- | --

#### Heating Circuits
The main circuit is HC0, this is linked to the main pump but some details in this circuit are hidden if any of HC1 to HC6 optional circuits are installed.

HC1 to HC6 are used to provide things like heating/ cooling to different room zones or multiple water tanks for hot water.

HC0 to HC6 usually have room thermostat's installed, if used for heating/ cooling, in this case there is a pad sub-section that contains ambient temperatures and humidity.  If not installed then there is an int (internal) sub-section that has the ambient temperatures.

Entity | Type | Description
-- | -- | --
name | sensor | The name of the circuit, hc0 is usually Home
on | Swtich | If the circuit is turns on or not
cooling | Binary Sensor | Circuit is in cooling mode
circulation_valve | Binary Sensor | If this circuit is requesting then this is open, this also triggers the main circulation pump
water_requested | Sensor | The requested water temperature based on heating and cooling curves
water_temp | Sensor | The actual water temperature for the circuit
auto | Sensor | No idea, it can be set on the thermostats but not sure what it does.
int.ambient_temp | Sensor | Internal ambient temperature, not really used.
int.ambient_requested | Sensor | Internal requested temperature not really used.
pad.current_humidity | Sensor | Room Humidity
pad.ambient_temp | Sensor | Room Thermostat Ambient Temperature
pad.ambient_requested | Sensor | Room Thermostat Requested Temperature

#### Pool and Solar
Some entities have been added based on debugging and best guess.


## Contributions are welcome!
If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

Also to determine mappings use the mastertherm connect module directly from the command line where you can get a list of current registers for your heatpump.


***

[masterthermimg]: mastertherm.png
[mastertherm]: https://github.com/sHedC/homeassistant-mastertherm
[commits-shield]: https://img.shields.io/github/commit-activity/y/sHedC/homeassistant-mastertherm?style=for-the-badge
[commits]: https://github.com/shedc/homeassistant-mastertherm/commits/main
[license-shield]: https://img.shields.io/github/license/sHedC/homeassistant-mastertherm.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Richard%20Holmes%20%40shedc-blue.svg?style=for-the-badge

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/


[releases]: https://github.com/shedc/homeassistant-mastertherm/releases
[stable-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-mastertherm?style=flat
[latest-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-mastertherm?include_prereleases&style=flat

[workflows]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/push.yml/badge.svg
[workflow-lastest]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/push.yml/badge.svg

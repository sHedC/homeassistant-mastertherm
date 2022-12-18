# mastertherm
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

**This component will set up the following platforms.**

To Be Complete!!!

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from mastertherm API.
`switch` | Switch something `True` or `False`.

![mastertherm][masterthermimg]

## NOTES:
This adds an integration to homeassistant (HACS) to connect to Mastertherm Heat Pumps.

There are two entry points for the Mastertherm Heat Pumps:
- mastertherm.vip-it.cz - This is the server for pre 2022 heat pumps
- mastertherm.online - This is the server for 2022 onward

NOTES:
- materhterm.online is sensitive to too many requests, for this reason by default it defaults to updates every 10 minutes, the App updates every 2 minutes. To help the Info updates every 30 min and data can be set in the options.
- if multiple requests are sent at the same time (i.e. from home assistant/ the app and web) some will be refused by the servers, its temporary.  The updates have been built to report but ignore these.

This is very beta, logging in works and 2 entities are returned per module

## Installation
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS.

At this time its not automatically part of HACS, so after installing HACS, visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-mastertherm.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

Once installed go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct mastertherm login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

Mastertherm only allows a single install, mutliple accounts are not currently supported.  Additionally if you have an installation with more than 2 units/ devices keep the refresh rate as 10 min or even increase it, the app/ web only connects to a single device/ unit at a time and refreshes every 2 minutes.

Local connection is not possible at this time, it seems the heat pumps connect to the servers using SSH.

#### Manual Install
To install manually, if you really want to:
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `mastertherm`.
4. Download _all_ the files from the `custom_components/mastertherm/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add the masterthermconnect module: pip install -I masterthermconnect
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

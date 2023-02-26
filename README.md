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
[![codecov][codecov-shield]][codecov-link]

Latest -
[![GitHub Release][latest-release-shield]][releases]
[![workflow-lastest]][workflows]
[![issues][issues-shield]][issues-link]

## Please Read
My friend who helps a lot with debugging and identifying details for this integration broke his system during this process and had to pay a couple of hundred Euros for it to be re-initialised. If you would like to support him to recover some of this please buy him a coffee.

SeBsZ Link: [![BuyMeCoffee][buymecoffeebadge]][buymecoffee_sebs]

If you feel like donating, my wife is rasing money for and the Salvation Army here:
<a href="https://www.justgiving.com/fundraising/jackie-holmes1933" target="_blank"><img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/salvationarmy.jpg?raw=true" alt="Charity Link" style="width:125px;height:20px;"></a>

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
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS, the integration will soon be part of the default integration.

Go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

<img src="/images/login.jpg" width="50%" height="50%">
<img src="/images/options.jpg" width="50%" height="50%">

#### Beta Versions
If you want to see Beta versions open the Mastertherm in HACS, after download, and click the three dots on the top right and select re-download. Here you will se an option to see beta versions.

#### If Not Available in HACS Yet
If you do the above and Mastertherm is not there it means its not yet been accepted into the default repository, hopfully this will only be a couple of weeks. In this case:

Visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-mastertherm.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

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
Example View, I don't have thermostats so not shown here.
<img src="/images/dashboard.jpg" width="50%" height="50%">

## Sensor Details
What is avaialbe in the app should be available here plus some extras.  There are controls in place to set the min and max values based on what is configured in your heatpump, in addition some features show or are hidden based on your setup, for example if cooling is not installed or disabled it is not shown in Home Assistant.

> :warning: **Heat Pump Configuration Changes:** Changing the configuration of the pump should only be done under the advise of your installer, the changes avaialable to home assistant are based only on the APP UI and some additional from the Thermostats if installed.

A lot of the temperature and modifiable settings have limits that come from the Heatpump, if you want to change these you should speak to your installer.

#### Main Circuit
This section covers entities that are linked tot he Main Heatpump, not all sensors will show up in your configuration depending on your installed configuration.

Entity | Type | Description
-- | -- | --
hp_power_state | Switch | Turn on and off the Heat Pump
hp_function | Select | The function is heating/ cooling or auto
operating_mode | Sensor | The current Operating Mode which shows 5 states: heating/ cooling/ pool/ hot water and defrost protection
cooling_mode | Binary Sensor | Whether the pump is in cooling mode or not (if not its heating)
compressor_running | Binary Sensor | Main compressor running
compressor2_running | Binary Sensor | Compressor 2 if installed
circulation_pump_running | Binary Sensor | Circulating water to where it is being requested, this is always true if any circuit is requesting heating or cooling
fan_running | Binary Sensor | The brine is ciculating for ground source or the fan is running for air source
defrost_mode | Binary Sensor | If the heat pump is in defrost mode
aux_heater_1 | Binary Sensor | If installed indicates if the auxillary heater is on
aux_heater_2 | Binary Sensor | If installed indicates if the second auxillary heater is on
outside_temp | Sensor | The outside temperature
requested_temp | Sensor | This is the temperature that the heat pump is requesting, it is calcuated by an unknown algorithm and can go higher than expected. An example here is when heating is initially requested it goes higher than needed then reduces as room temperature is reached.
actual_temp | Sensor | The actual temperature that the heat pump is up to.
dewp_control | Binary Sensor | If Dew Point Control is active
high_tariff_control | Binary Sensor | If the feature is enabled then this will show enabled if the system recognized high tariff.  This feature (called HDO_ON) is actually a remote on/off for features on your heatpump that use high energy such as the compressor/ aux heaters and sanitary hot water feature.  It does not disable the DHW function, which also uses the compressor. This feature is really only of use where your have variying high/ low tariff during the day and night or extended periods of low tariff as it disabled heating.

#### Season Info
Entity | Type | Description
-- | -- | --
mode | Sensor | The Season mode the heatpump is running on, winter/ summer/ auto winter or auto summer.
select | Select | Ability to select the mode, Auto, Winter or Summer
winter_temp | Number | The temperature below which is considered winter
summer_temp | Number | The temperature above which is considered winter

#### Control Curves Heating/ Cooling
These are the min and max values to control the heating and cooling curves used by the Heatpump to control the warter temperature.

Entity | Type | Description
-- | -- | --
setpoint_a_outside | Number | Outside Temperature for Setpoint A, min/ max values are controlled by pump configuration.
setpoint_a_requested | Number | Temperature to set for Setpoint A, min/ max values are controlled by pump configuration.
setpoint_b_outside | Number | Outside Temperature for Setpoint B, min/ max values are controlled by pump configuration.
setpoint_b_requested | Number | Temperature to set for Setpoint B, min/ max values are controlled by pump configuration.


#### Domestic Hot Water
Entity | Type | Description
-- | -- | --
heating | Binary Sensor | Whether hot water is requested, also activates if HC1 to 6 is for hot water
enabled | Binary Sensor | Not sure on mine always shows disabled.
current_temp | Sensor | The current temperature of the hot water, should be taken from the sensor in the water tank
required_temp | Sensor | The temperature that was set as required for your hot water, min/ max values are controlled by pump configuration.

#### Run Time Info
Entity | Type | Description
-- | -- | --
compressor_run_time | Sensor | Number of hours the compressor has run for
compressor_start_counter | Sensor | Probably the number of times the compressor has started
pump_runtime | Sensor | The number of hours the circulation pump has run
aux1_runtime | Sensor | The house the auxillary heaters have run
aux2_runtime | Sensor | The house the auxillary heaters have run

#### Error Info
Shows Error Alerts, Not Documented at this time.

Entity | Type | Description
-- | -- | --
some_errror | BinarySensor | No Information Yet
three_errors | BinarySensor | No Information Yet
reset_3e | BinarySensor | No Information Yet
safety_tstat | BinarySensor | No Information Yet


#### Heating Circuits
The main circuit is HC0, this is linked to the main pump but some details in this circuit are hidden if any of HC1 to HC6 optional circuits are installed.

HC1 to HC6 are used to provide things like heating/ cooling to different room zones or multiple water tanks for hot water.

HC0 to HC6 may have room thermostat's installed, if used for heating/ cooling, in this case there is a pad sub-section that contains ambient temperatures and humidity.  If not installed then there is an int (internal) sub-section that has the ambient temperatures.

Entity | Type | Description
-- | -- | --
name | sensor | The name of the circuit, hc0 is usually Home
on | Swtich | If the circuit is turns on or not
cooling | Binary Sensor | Circuit is in cooling mode
circulation_valve | Binary Sensor | If this circuit is requesting then this is open, this also triggers the main circulation pump
water_requested | Sensor | The requested water temperature based on heating and cooling curves
water_temp | Sensor | The actual water temperature for the circuit
auto | Sensor | I believe this controls if the water temperature requested is manually set or automatic based ont he heating/ cooling curves.
ambient_temp | Sensor | Ambient temperature, either from the room if the pad is installed or internal
ambient_requested | Sensor | requested temperature, either from the room if the pad is installed or internal
thermostat | Climate | Allows setting of the room temperature settings.
pad.state | Sensor | The Room pad state
pad.current_humidity | Sensor | Room Humidity, if the thermostat is installed
control_curve_heating | None | Same as the main control curve heating
control_curve_cooling | None | Same as the main control curve cooling

#### Pool and Solar
Solar monitors outside temperature and if enabled can be used to turn on and off the hot water on the heat pump.  Used if you have PV hot water installed.

Pool monitors and sets the pool temperature.

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
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
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

# Mastertherm
[![License][license-shield]](LICENSE) ![Project Maintenance][maintenance-shield] [![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs] [![Discord][discord-shield]][discord] [![Community Forum][forum-shield]][forum] [![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Stable -
[![GitHub Release][stable-release-shield]][releases] [![workflow-release]][workflows-release] [![codecov][codecov-shield]][codecov-link]

Latest -
[![GitHub Release][latest-release-shield]][releases] [![workflow-lastest]][workflows] [![issues][issues-shield]][issues-link]

## Please Read
My friend who helps a lot with debugging and identifying details for this integration broke his system during this process and had to pay a couple of hundred Euros for it to be re-initialised. If you would like to support him to recover some of this please buy him a coffee.

SeBsZ Link: [![BuyMeCoffee][buymecoffeebadge_sebs]][buymecoffee_sebs]

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

{% if not installed %}

## Installation
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS, the integration will soon be part of the default integration.

Go to HACS and integraitons, then select to download Mastertherm from HACS.

#### If Not Available in HACS Yet
If you do the above and Mastertherm is not there it means its not yet been accepted into the default repository, hopfully this will only be a couple of weeks. In this case:

Visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-mastertherm.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

{% endif %}

## Configuration
Go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

Updating Options immediately after setup may cause an error in the logs, this can be ignored.

<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/login.jpg?raw=true" width="50%" height="50%">
<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/options.jpg?raw=true" width="50%" height="50%">

#### Beta Versions
If you want to see Beta versions open the Mastertherm in HACS, after download, and click the three dots on the top right and select re-download. Here you will se an option to see beta versions.

## Sensor Details
See Git Hub Mastertherm Repository for more information: [HASS Mastertherm][mastertherm]

## Example HASS View
Example View, I don't have thermostats so they are not shown here:
<img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/dashboard.jpg?raw=true">

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
[workflows-release]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/release.yml/badge.svg
[workflow-release]: https://github.com/sHedC/homeassistant-mastertherm/actions/workflows/release.yml/badge.svg

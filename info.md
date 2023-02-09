# Mastertherm
[![License][license-shield]](LICENSE) ![Project Maintenance][maintenance-shield] [![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs] [![Discord][discord-shield]][discord] [![Community Forum][forum-shield]][forum]

Stable -
[![GitHub Release][stable-release-shield]][releases]

Latest -
[![GitHub Release][latest-release-shield]][releases] [![workflow-lastest]][workflows]

## About
If you feel like donating, my wife is rasing money for and the Salvation Army here:
<a href="https://www.justgiving.com/fundraising/jackie-holmes1933" target="_blank"><img src="https://github.com/sHedC/homeassistant-mastertherm/blob/main/images/salvationarmy.jpg?raw=true" alt="Charity Link" style="width:250px;height:40px;"></a>

![mastertherm][masterthermimg]

This adds an integration to homeassistant (HACS) to connect to Mastertherm Heat Pumps. There are two entry points for the Mastertherm Heat Pumps:
- mastertherm.vip-it.cz - This is the server for pre 2022 heat pumps
- mastertherm.online - This is the server for 2022 onward

NOTES:
- materhterm.online is sensitive to too many requests, for this reason by default it defaults to updates every 2 minutes, the App updates every 30 seconds. To help the Info updates every 30 min, data can be set in the options down to 30 seconds.
- if multiple requests are sent at the same time (i.e. from home assistant/ the app and web) some will be refused by the servers, its temporary.  The updates have been built to report but ignore these.

{% if not installed %}

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
6. Add the masterthermconnect module: pip install -I masterthermconnect==1.2.0
7. Restart Home Assistant
8. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"

{% endif %}

## Configuration is done in the UI

## Sensor Details
See Git Hub Mastertherm Repository for more information: ![Mastertherm Hass Github][mastertherm]

***

[masterthermimg]: https://github.com/sHedC/homeassistant-mastertherm/raw/main/mastertherm.png
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

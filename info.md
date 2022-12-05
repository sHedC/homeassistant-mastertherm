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

{% if not installed %}

## Installation
The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS.

At this time its not automatically part of HACS, so after installing HACS, visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-mastertherm.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

Once installed go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Mastertherm"
- Select the correct mastertherm login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options

Mastertherm only allows a single install, mutliple accounts are not currently supported.  Additionally if you have an installation with more than 2 units/ devices keep the refresh rate as 10 min or even increase it, the app/ web only connects to a single device/ unit at a time and refreshes every 2 minutes.

Local connection is not possible at this time, it seems the heat pumps connect to the servers using SSH.

{% endif %}

## Configuration is done in the UI

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

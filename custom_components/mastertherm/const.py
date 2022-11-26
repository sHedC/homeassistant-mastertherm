"""Constants used by Home Assistant Components."""
from homeassistant.const import Platform

NAME = "Mastertherm"
DOMAIN = "mastertherm"

API_VERSIONS = {
    "v1": ("mastertherm.vip-it.cz (Pre 2022)", "V1"),
    "v2": ("mastertherm.online (Post 2022)", "V2"),
}

# Platforms
PLATFORMS = [Platform.SENSOR]

"""Global fixtures for mastertherm integration."""
from unittest.mock import patch

import pytest

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_TOKEN,
    CONF_USERNAME,
)

from custom_components.mastertherm.const import DOMAIN

TEST_MODULES = [
    {
        "id": "1234",
        "module_name": "MasterTherm_1234",
        "config": [
            {
                "mb_addr": "1",
                "mb_name": "Module_Board_1",
            },
        ],
    },
]
TEST_AUTHRESULT = {
    CONF_TOKEN: "token",
    "expires": "yyyy-mm-dd hh:mm:ss ZZZ",
    "modules": TEST_MODULES,
    "role": "400",
}

TEST_CONFIGDATA = {
    DOMAIN: {
        CONF_USERNAME: "user.name",
        CONF_PASSWORD: "hash",
    }
}

TEST_ENTITIES = {
    "modules": {
        "1234_1": {
            "info": {
                "module_id": "1234",
                "user_name": "UserName",
                "module_name": "1234_Serial_UserName_XX_CC_Thermal",
                "serial_number": "Serial",
                "module_type": "Thermal",
                "location": "XX",
                "country": "CC",
                "mb_addr": "1",
                "mb_name": "Module_Board_1",
            },
            "entities": {
                "outside_temp": {
                    "type": "temperature",
                    "name": "Outside Temperature",
                    "state": 8.4,
                }
            },
        }
    }
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations,
):  # pylint: disable=unused-argument
    """This ficture enables loading custom integrations in all tess."""
    yield


@pytest.fixture
def mock_configdata():
    """Return a default mock configuration."""
    return TEST_CONFIGDATA


@pytest.fixture
def mock_authresult():
    """Return a default mock authentication result."""
    return TEST_AUTHRESULT


@pytest.fixture
def mock_moduledata():
    """Return a default mock module data."""
    return TEST_MODULES


@pytest.fixture
def mock_entitydata():
    """Returns a default set of Entities."""
    return TEST_ENTITIES


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
# @pytest.fixture(name="skip_notifications", autouse=True)
# def skip_notifications_fixture():
#    """Skip notification calls."""
#    with patch("homeassistant.components.persistent_notification.async_create"), patch(
#        "homeassistant.components.persistent_notification.async_dismiss"
#    ):
#        yield

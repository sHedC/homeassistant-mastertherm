"""Global fixtures for mastertherm integration."""
import json
import os
from unittest.mock import patch
import pytest

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_TOKEN,
    CONF_USERNAME,
    CONF_API_VERSION,
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
    DOMAIN: {CONF_USERNAME: "user.name", CONF_PASSWORD: "hash", CONF_API_VERSION: "v1"}
}

TEST_ENTITIES = {
    "modules": {
        "1234_1": {
            "info": {
                "unit_id": "1234",
                "user_name": "UserName",
                "module_name": "1234_AQI4434344_UserName_XX_CC_Thermal",
                "serial_number": "AQI4434344",
                "output": "EM45",
                "hp_type": "Thermal",
                "location": "XX",
                "country": "CC",
                "mb_addr": "1",
                "mb_name": "Module_Board_1",
                "api_url": "https://mastertherm.vip-it.cz",
                "version": "2.1.0",
            },
            "entities": {
                "hp_type": 1,
                "hp_power_state": True,
                "operating_mode": "idle",
                "season.mode": "auto-winter",
                "season.manual_set": False,
                "season.winter": True,
                "season.winter_temp": 11.0,
                "season.summer_temp": 14.0,
                "compressor_running": True,
                "hp_function": 0,
                "outside_temp": 8.4,
            },
        }
    }
}


def load_fixture(folder, filename):
    """Load a JSON fixture for testing."""
    try:
        path = os.path.join(os.path.dirname(__file__), "fixtures", folder, filename)
        with open(path, encoding="utf-8") as fptr:
            return fptr.read()
    except OSError:
        return None


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations,
):  # pylint: disable=unused-argument
    """Ficture enables loading custom integrations in all tess."""
    yield


class APIMock:
    """Mock up the API responses."""

    error = ""

    def __init__(self):
        """Initialize the Mock API."""

    async def connect(self):
        """Simulate the Connect and Update method."""
        return True

    def refresh(self, full_load=False):  # pylint: disable=unused-argument
        """Mock the Refresh Method."""
        return True

    def get_devices(self):
        """Return a list of devices."""
        info = json.loads(load_fixture("masterthermconnect", "device_list.json"))
        if info is None:
            info = {}

        return info

    def get_device_data(self, module_id: str, unit_id: str):
        """Return the data for the device."""
        info = json.loads(
            load_fixture(
                "masterthermconnect", f"device_data_{module_id}_{unit_id}.json"
            )
        )
        if info is None:
            info = {}
        elif self.error == "offline":
            info["operating_mode"] = "offline"

        return info

    # pylint: disable=unused-argument
    async def set_device_data_item(
        self, module_id: str, unit_id: str, entry: str, value: any
    ) -> bool:
        """Set the Device Data."""
        return True


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
    """Return a default set of Entities."""
    return TEST_ENTITIES


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield

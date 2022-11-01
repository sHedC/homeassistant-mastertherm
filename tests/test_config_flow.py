"""Test mastertherm config flow."""
from unittest.mock import patch
import pytest

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_TOKEN, CONF_USERNAME

from custom_components.mastertherm.const import DOMAIN


@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """This fixture bypasses the actual setup of the integration
    since we only want to test the config flow. We test the
    actual functionality of the integration in other test modules."""
    with patch("custom_components.mastertherm.async_setup", return_value=True,), patch(
        "custom_components.mastertherm.async_setup_entry",
        return_value=True,
    ):
        yield


async def test_form_success(
    hass: HomeAssistant, mock_authresult: tuple[dict, dict], mock_moduledata: dict
):
    """Test setting up the form and configuring."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "success"}, mock_authresult),
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name"}
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert setup_result["title"] == "user.name"
    assert setup_result["data"][CONF_TOKEN] == mock_authresult[CONF_TOKEN]
    assert setup_result["data"]["expires"] == mock_authresult["expires"]
    assert setup_result["data"]["modules"] == mock_moduledata

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant):
    """Test Form Login with Invalid Authentication."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "authentication_error"}, {}),
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name"}
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert setup_result["step_id"] == "user"
    assert setup_result["errors"] == {"base": "authentication_error"}

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_cannot_connect(hass: HomeAssistant):
    """Test Form Login where connection is not avaialble."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "connection_error"}, {}),
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name"}
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert setup_result["step_id"] == "user"
    assert setup_result["errors"] == {"base": "connection_error"}

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_duplicate(hass: HomeAssistant, mock_authresult: dict):
    """Test Form Login with user already set up."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Setup the User first Time
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "success"}, mock_authresult),
    ), patch("custom_components.mastertherm.async_setup", return_value=True), patch(
        "custom_components.mastertherm.async_setup_entry", return_value=True
    ):
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name"}
        )
        await hass.async_block_till_done()

    assert setup_result["title"] == "user.name"

    # Setup the User second Time
    result2 = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "success"}, mock_authresult),
    ):
        setup_result2 = await hass.config_entries.flow.async_configure(
            result2["flow_id"], {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name"}
        )
        await hass.async_block_till_done()

    assert setup_result2["type"] == data_entry_flow.RESULT_TYPE_ABORT
    assert setup_result2["reason"] == "already_configured"


async def test_import_config(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_authresult: dict,
    mock_moduledata: dict,
):
    """Peform an import flow setup."""
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value=({"status": "success"}, mock_authresult),
    ) as mock_authenticate, patch(
        "custom_components.mastertherm.async_setup", return_value=True
    ) as mock_setup, patch(
        "custom_components.mastertherm.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data=mock_configdata[DOMAIN],
        )
        await hass.async_block_till_done()

    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "user.name"
    assert result["data"][CONF_TOKEN] == mock_authresult[CONF_TOKEN]
    assert result["data"]["expires"] == mock_authresult["expires"]
    assert result["data"]["modules"] == mock_moduledata

    assert len(mock_authenticate.mock_calls) == 1
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1

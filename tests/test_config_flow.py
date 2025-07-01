"""Test mastertherm config flow."""
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_API_VERSION,
    CONF_SCAN_INTERVAL,
)

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mastertherm.const import DOMAIN


async def test_form_success(hass: HomeAssistant):
    """Test setting up the form and configuring."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name", CONF_API_VERSION: "v1"},
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert setup_result["title"] == "user.name"

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant):
    """Test Form Login with Invalid Authentication."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "authentication_error"},
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name", CONF_API_VERSION: "v1"},
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert setup_result["step_id"] == "user"
    assert setup_result["errors"] == {"base": "authentication_error"}

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_reauth(hass: HomeAssistant):
    """Test Form Login Re-authentication."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_PASSWORD: "hash",
            CONF_USERNAME: "user.name",
            CONF_API_VERSION: "v1",
        },
        unique_id="111010202002020",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_REAUTH,
            "entry_id": entry.entry_id,
        },
        data=entry.data,
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch("custom_components.mastertherm.async_setup", return_value=True), patch(
        "custom_components.mastertherm.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PASSWORD: "new-test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "abort"
    assert result2["reason"] == "reauth_successful"


async def test_form_cannot_connect(hass: HomeAssistant):
    """Test Form Login where connection is not avaialble."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "connection_error"},
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name", CONF_API_VERSION: "v1"},
        )
        await hass.async_block_till_done()

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert setup_result["step_id"] == "user"
    assert setup_result["errors"] == {"base": "connection_error"}

    assert len(mock_authenticate.mock_calls) == 1


async def test_form_single_instance(hass: HomeAssistant):
    """Test Form Login with single instance."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Setup the User first Time
    with patch(
        "custom_components.mastertherm.config_flow.authenticate",
        return_value={"status": "success"},
    ), patch("custom_components.mastertherm.async_setup", return_value=True), patch(
        "custom_components.mastertherm.async_setup_entry", return_value=True
    ):
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "hash", CONF_USERNAME: "user.name", CONF_API_VERSION: "v1"},
        )
        await hass.async_block_till_done()

    assert setup_result["title"] == "user.name"

    # Setup the User second Time
    result2 = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result2["type"] == data_entry_flow.FlowResultType.ABORT
    assert result2["reason"] == "single_instance_allowed"


async def test_update_options(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_entitydata: dict,
):
    """Test updating the option reloads correctly."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    with patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ) as mock_updater:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."

    # show user form
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Populate with updated options
    with patch(
        (
            "custom_components.mastertherm.coordinator."
            "MasterthermDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_entitydata,
    ) as mock_updater:
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={CONF_SCAN_INTERVAL: 30},
        )
        await hass.async_block_till_done()

    assert result["type"] == "create_entry"
    assert result["result"] is True

    # Check the Refresh Interval was updated
    assert entry.options.get(CONF_SCAN_INTERVAL) == 30

"""MasterTherm Config Flow."""
import logging
from typing import Any
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
    CONN_CLASS_CLOUD_POLL,
)
from homeassistant.core import callback
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_API_VERSION,
    CONF_SCAN_INTERVAL,
)
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_FULL_REFRESH,
    CONF_REFRESH_OFFSET,
    DOMAIN,
    DEFAULT_FULL_REFRESH,
    DEFAULT_REFRESH_OFFSET,
    API_VERSIONS,
    DEFAULT_REFRESH,
)
from .coordinator import authenticate

_LOGGER = logging.getLogger(__name__)

MASTERTHERM_OUR = {""}
DEFAULT_PORT = 80


class MasterthermFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MasterTherm."""

    # Used to call the migration method if the verison changes.
    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize the Masterhterm Flow."""
        self.reauth_entry: ConfigEntry | None = None
        self._errors = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        # only a single instance of the integration is allowed:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            user_input = {}
            user_input[CONF_USERNAME] = ""
            user_input[CONF_PASSWORD] = ""
            user_input[CONF_API_VERSION] = ""

            return await self._show_config_form(user_input)

        auth_result = await authenticate(
            user_input[CONF_USERNAME],
            user_input[CONF_PASSWORD],
            user_input[CONF_API_VERSION],
        )

        if auth_result["status"] != "success":
            # Show the Config Form again with the error
            self._errors["base"] = auth_result["status"]
            return await self._show_config_form(user_input)

        # Setup the Unique ID and check if already configured
        await self.async_set_unique_id(user_input[CONF_USERNAME])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

    async def async_step_reauth_confirm(
        self,
        user_input: dict[str, Any] | None = None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Handle reauth confirmation."""
        assert self.reauth_entry is not None

        # if there is no user input then re-direct the user step.
        if user_input is not None:
            entry_data = self.reauth_entry.data

            auth_result = await authenticate(
                entry_data[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                entry_data[CONF_API_VERSION],
            )

            if auth_result["status"] == "success":
                self.hass.config_entries.async_update_entry(
                    self.reauth_entry, data={**entry_data, **user_input}
                )
                await self.hass.config_entries.async_reload(self.reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_PASSWORD): cv.string}),
            errors=self._errors,
        )

    async def async_step_reauth(
        self, user_input: dict[str, Any]  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Handle configuration by re-auth."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the option flow handler."""
        return MasterthermOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input: dict[str, Any]):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_VERSION, default=user_input[CONF_API_VERSION]
                    ): vol.In(API_VERSIONS),
                    vol.Required(
                        CONF_USERNAME, default=user_input[CONF_USERNAME]
                    ): cv.string,
                    vol.Required(
                        CONF_PASSWORD, default=user_input[CONF_PASSWORD]
                    ): cv.string,
                }
            ),
            errors=self._errors,
        )


class MasterthermOptionsFlowHandler(OptionsFlow):
    """Mastertherm config options flow handler."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH),
                    ): vol.All(vol.Coerce(int), vol.Range(min=30)),
                    vol.Required(
                        CONF_FULL_REFRESH,
                        default=self.options.get(
                            CONF_FULL_REFRESH, DEFAULT_FULL_REFRESH
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=360)),
                    vol.Required(
                        CONF_REFRESH_OFFSET,
                        default=self.options.get(
                            CONF_REFRESH_OFFSET, DEFAULT_REFRESH_OFFSET
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=30)),
                }
            ),
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )

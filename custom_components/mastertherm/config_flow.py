"""MasterTherm Config Flow."""
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_API_VERSION,
    CONF_SCAN_INTERVAL,
)

from .const import DOMAIN, API_VERSIONS, DEFAULT_REFRESH
from .coordinator import authenticate

_LOGGER = logging.getLogger(__name__)

MASTERTHERM_OUR = {""}
DEFAULT_PORT = 80


class MasterthermFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MasterTherm."""

    # Used to call the migration method if the verison changes.
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MasterthermOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input: dict):
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


class MasterthermOptionsFlowHandler(config_entries.OptionsFlow):
    """Mastertherm config options flow handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
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
                    ): vol.All(vol.Coerce(int), vol.Range(min=30))
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )

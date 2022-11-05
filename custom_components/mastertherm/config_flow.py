"""MasterTherm Config Flow."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN
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

    async def async_step_import(self, user_input=None):
        """Import a config entry from configuraiton.yaml."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is None:
            user_input = {}
            user_input[CONF_USERNAME] = ""
            user_input[CONF_PASSWORD] = ""

            return await self._show_config_form(user_input)

        auth_result = await authenticate(
            self.hass, user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
        )

        if auth_result["status"] != "success":
            # Show the Config Form again with the error
            self._errors["base"] = auth_result["status"]
            return await self._show_config_form(user_input)

        # Setup the Unique ID and check if already configured
        await self.async_set_unique_id(user_input[CONF_USERNAME])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

    async def _show_config_form(self, user_input: dict):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

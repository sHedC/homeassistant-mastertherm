"""MasterTherm Config Flow."""
from copy import deepcopy
from typing import Any

import probatio

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
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
    ) -> ConfigFlowResult:
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
    ) -> ConfigFlowResult:
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
            data_schema=probatio.Schema({probatio.Required(CONF_PASSWORD): str}),
            errors=self._errors,
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle configuration by re-auth."""
        _ = entry_data
        self.reauth_entry = self._get_reauth_entry()
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
            data_schema=probatio.Schema(
                {
                    probatio.Required(
                        CONF_API_VERSION, default=user_input[CONF_API_VERSION]
                    ): probatio.In(API_VERSIONS),
                    probatio.Required(
                        CONF_USERNAME, default=user_input[CONF_USERNAME]
                    ): str,
                    probatio.Required(
                        CONF_PASSWORD, default=user_input[CONF_PASSWORD]
                    ): str,
                }
            ),
            errors=self._errors,
        )


class MasterthermOptionsFlowHandler(OptionsFlow):
    """Mastertherm config options flow handler."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Mastertherm options flow."""
        # self.config_entry = config_entry
        self.options = deepcopy(dict(config_entry.options))

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Manage the options."""
        return await self.async_step_user(user_input)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.config_entry.data.get(CONF_USERNAME), data=self.options
            )

        return self.async_show_form(
            step_id="user",
            data_schema=probatio.Schema(
                {
                    probatio.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH),
                    ): probatio.All(probatio.Coerce(int), probatio.Range(min=30)),
                    probatio.Required(
                        CONF_FULL_REFRESH,
                        default=self.options.get(
                            CONF_FULL_REFRESH, DEFAULT_FULL_REFRESH
                        ),
                    ): probatio.All(
                        probatio.Coerce(int), probatio.Range(min=5, max=360)
                    ),
                    probatio.Required(
                        CONF_REFRESH_OFFSET,
                        default=self.options.get(
                            CONF_REFRESH_OFFSET, DEFAULT_REFRESH_OFFSET
                        ),
                    ): probatio.All(
                        probatio.Coerce(int), probatio.Range(min=0, max=30)
                    ),
                }
            ),
        )

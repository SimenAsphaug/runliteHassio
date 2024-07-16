import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured RuneLite instances."""
    return set(entry.data["name"] for entry in hass.config_entries.async_entries(DOMAIN))

class RuneLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RuneLite."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Validate the user input here if needed
            return self.async_create_entry(title=user_input["name"], data=user_input)

        # Show the form with placeholders
        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("token"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={
                "name": "Enter a name for this RuneLite instance",
                "token": "Enter your Home Assistant long-lived access token",
            },
            errors=errors,
        )

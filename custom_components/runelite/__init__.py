import logging
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)

DOMAIN = "runelite"

def setup(hass, config):
    """Set up the RuneLite integration."""
    hass.http.register_view(RuneLiteView)
    return True

class RuneLiteView(HomeAssistantView):
    """Handle incoming data from RuneLite."""

    url = "/api/runelite"
    name = "api:runelite"
    requires_auth = False

    async def post(self, request):
        """Handle POST request."""
        try:
            data = await request.json()
            state = data.get("state")
            attributes = data.get("attributes")

            # Update sensor state
            hass.states.async_set("sensor.farming_patch_example", state, attributes)
            return self.json({"success": True})
        except Exception as e:
            _LOGGER.error("Failed to process data from RuneLite: %s", e)
            return self.json({"success": False, "error": str(e)}, status_code=500)

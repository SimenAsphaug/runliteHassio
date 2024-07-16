import logging
from homeassistant.components.sensor import SensorEntity

DOMAIN = "runelite"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the RuneLite sensor from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([RuneLiteSensor(config["name"], config["home_assistant_url"], config["token"])])


class RuneLiteSensor(SensorEntity):
    """Representation of a RuneLite sensor."""

    def __init__(self, name, home_assistant_url, token):
        self._name = name
        self._state = None
        self._attributes = {}
        self._home_assistant_url = home_assistant_url
        self._token = token

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(f"{self._home_assistant_url}/api/states/sensor.farming_patch_example", headers={"Authorization": f"Bearer {self._token}"})
            data = response.json()
            self._state = data["state"]
            self._attributes = data["attributes"]
        except Exception as e:
            _LOGGER.error("Failed to update sensor: %s", e)

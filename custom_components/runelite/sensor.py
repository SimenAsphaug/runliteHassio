import logging
import requests
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the RuneLite sensor."""
    add_entities([RuneLiteSensor()])


class RuneLiteSensor(SensorEntity):
    """Representation of a RuneLite sensor."""

    def __init__(self):
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Farming Patch Example"

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
            response = requests.get("http://runelite.local/api/farming")
            data = response.json()
            self._state = data["state"]
            self._attributes = data["attributes"]
        except Exception as e:
            _LOGGER.error("Failed to update sensor: %s", e)

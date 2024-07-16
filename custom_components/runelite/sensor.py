import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the RuneLite sensor from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    session = async_get_clientsession(hass)
    
    # List of sensor types
    sensor_types = ["herbs", "trees", "allotments"]
    
    # Use the internal URL from Home Assistant configuration
    internal_url = hass.config.internal_url

    # Fetch token from the configuration entry
    token = config_entry.data.get("token")
    
    # Create sensor entities for each type
    sensors = [RuneLiteSensor(config["name"], internal_url, token, session, sensor_type) for sensor_type in sensor_types]
    async_add_entities(sensors, update_before_add=True)


class RuneLiteSensor(SensorEntity):
    """Representation of a RuneLite sensor."""

    def __init__(self, name, home_assistant_url, token, session, patch_type):
        self._name = f"{name} {patch_type.capitalize()} Patch"
        self._state = None
        self._attributes = {}
        self._home_assistant_url = home_assistant_url
        self._token = token
        self._session = session
        self._patch_type = patch_type

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

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            url = f"{self._home_assistant_url}/api/states/sensor.farming_patch_{self._patch_type}"
            headers = {"Authorization": f"Bearer {self._token}"}
            async with self._session.get(url, headers=headers) as response:
                data = await response.json()
                self._state = data["state"]
                self._attributes = data["attributes"]
        except Exception as e:
            _LOGGER.error("Failed to update sensor: %s", e)

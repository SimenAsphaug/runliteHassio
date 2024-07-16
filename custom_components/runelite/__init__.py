import logging
from homeassistant.helpers import config_entry_flow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the RuneLite integration."""
    return True

async def async_setup_entry(hass, entry):
    """Set up RuneLite from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

"""KWK Index integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_SOURCE_URL, DOMAIN, FALLBACK_KWK_XLSX_URL
from .coordinator import KwkIndexCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type KwkIndexConfigEntry = ConfigEntry[KwkIndexCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: KwkIndexConfigEntry) -> bool:
    """Set up KWK Index from a config entry."""
    coordinator = KwkIndexCoordinator(
        hass,
        source_url=entry.options.get(
            CONF_SOURCE_URL,
            entry.data.get(CONF_SOURCE_URL, FALLBACK_KWK_XLSX_URL),
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: KwkIndexConfigEntry) -> bool:
    """Unload a KWK Index config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

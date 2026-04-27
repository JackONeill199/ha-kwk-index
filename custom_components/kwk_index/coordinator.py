"""Data coordinator for the KWK Index integration."""

from __future__ import annotations

from dataclasses import dataclass
import logging
import re

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    EEX_DOWNLOADS_URL,
    EEX_INDICES_URL,
    FALLBACK_KWK_XLSX_URL,
)
from .parser import KwkIndexValue, parse_kwk_xlsx

_KWK_XLSX_RE = re.compile(
    r"https://www\.eex\.com/fileadmin/[^\"']+?_KWK\.xlsx", re.IGNORECASE
)
_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class KwkIndexData:
    """Latest KWK index data."""

    value: KwkIndexValue
    source_url: str


class KwkIndexCoordinator(DataUpdateCoordinator[KwkIndexData]):
    """Coordinate KWK Index updates."""

    def __init__(self, hass: HomeAssistant, source_url: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self._configured_source_url = source_url

    async def _async_update_data(self) -> KwkIndexData:
        """Fetch and parse the newest KWK index file."""
        session = async_get_clientsession(self.hass)

        try:
            source_url = await self._async_find_source_url(session)
            response = await session.get(source_url, timeout=30)
            response.raise_for_status()
            content = await response.read()
        except (ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Could not fetch KWK index XLSX: {err}") from err

        try:
            value = parse_kwk_xlsx(content)
        except ValueError as err:
            raise UpdateFailed(f"Could not parse KWK index XLSX: {err}") from err

        return KwkIndexData(value=value, source_url=source_url)

    async def _async_find_source_url(self, session) -> str:
        """Return a KWK XLSX URL, preferring the newest link from EEX pages."""
        if self._configured_source_url != FALLBACK_KWK_XLSX_URL:
            return self._configured_source_url

        for page_url in (EEX_INDICES_URL, EEX_DOWNLOADS_URL):
            try:
                response = await session.get(page_url, timeout=30)
                response.raise_for_status()
                html = await response.text()
            except (ClientError, TimeoutError):
                continue

            matches = _KWK_XLSX_RE.findall(html)
            if matches:
                return matches[0]

        return self._configured_source_url

"""Constants for the KWK Index integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "kwk_index"

DEFAULT_NAME = "KWK Baseloadpreis"
DEFAULT_SCAN_INTERVAL = timedelta(hours=12)

EEX_INDICES_URL = "https://www.eex.com/en/market-data/indices-benchmark/indices"
EEX_DOWNLOADS_URL = "https://www.eex.com/en/downloads"
FALLBACK_KWK_XLSX_URL = (
    "https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/"
    "EEX_Group_DataSource/KWK/20260401_KWK.xlsx"
)

CONF_SOURCE_URL = "source_url"

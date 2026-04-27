"""Sensor platform for KWK Index."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import KwkIndexCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[KwkIndexCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up KWK Index sensors."""
    async_add_entities([KwkBaseloadPriceSensor(entry)])


class KwkBaseloadPriceSensor(CoordinatorEntity[KwkIndexCoordinator], SensorEntity):
    """Sensor exposing the latest KWK baseload price."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_unit_of_measurement = f"ct/{UnitOfEnergy.KILO_WATT_HOUR}"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:transmission-tower"

    def __init__(self, entry: ConfigEntry[KwkIndexCoordinator]) -> None:
        """Initialize the sensor."""
        super().__init__(entry.runtime_data)
        self._attr_unique_id = f"{DOMAIN}_baseload_price"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)},
            "name": DEFAULT_NAME,
            "manufacturer": "EEX",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> float:
        """Return the current KWK price in ct/kWh."""
        return self.coordinator.data.value.price_ct_per_kwh

    @property
    def extra_state_attributes(self) -> dict[str, str | float | int]:
        """Return additional KWK index details."""
        value = self.coordinator.data.value
        return {
            "quarter": value.quarter,
            "quarter_number": value.quarter_number,
            "year": value.year,
            "price_eur_per_mwh": value.price_eur_per_mwh,
            "source": self.coordinator.data.source_url,
        }

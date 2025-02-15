"""Platform for Divoom Bluetooth Score integration."""
from __future__ import annotations


from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_MAC
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from .devices.pixoo import Pixoo
from .const import DOMAIN, ATTR_SCORE_1, ATTR_SCORE_2, CONF_DEVICE_TYPE
from homeassistant.components.number import (
    NumberEntity,
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Divoom Bluetooth Number Score based on config entry"""
    if entry is None:
        return

    data = {
        "name": entry.title,
        "mac": entry.data[CONF_MAC],
        "device_type": entry.data[CONF_DEVICE_TYPE],
    }

    divoomBluetoothDevice = hass.data[DOMAIN]["divoom_device"]

    async_add_entities([ScoreNumber(1, data, divoomBluetoothDevice), ScoreNumber(2, data, divoomBluetoothDevice)])

#def setup_platform(
#    hass: HomeAssistant,
#    config: ConfigType,
#    add_entities: AddEntitiesCallback,
#    discovery_info: DiscoveryInfoType | None = None
#) -> None:
#    """Set up the Score platform."""
#    if discovery_info is None:
#        return
#
#    name = discovery_info[CONF_NAME]
#    device_type = discovery_info[CONF_DEVICE_TYPE]
#    mac = discovery_info[CONF_MAC]
#
#    add_entities([ScoreNumber(1, name, device_type, mac), ScoreNumber(2, name, device_type, mac)])

class ScoreNumber(NumberEntity):
    """Representation of a Score."""

    _attr_has_entity_name = True

    def __init__(self, num, data, divoomBluetoothDevice: Pixoo) -> None:
        name = data["name"]
        mac = data["mac"]
        device_type = data["device_type"]

        self._attr_name = "Score {}".format(num)
        self._num = num

        self._attr_unique_id = "{}-score-{}".format(mac, num)
        self._attr_max_value = 100
        self._attr_device_info = {
            "name": name,
            "manufacturer": "divoom",
            "model": device_type,
            "connections": {
                (dr.CONNECTION_BLUETOOTH, mac)
            }
        }

        self._divoomBluetoothDevice = divoomBluetoothDevice

    @property
    def state(self) -> float | None:
        if self._num == 1:
            return self._divoomBluetoothDevice.score_1
        elif self._num == 2:
            return self._divoomBluetoothDevice.score_2

    def set_native_value(self, value: float) -> None:
        self._attr_state = int(value)
        if self._num == 1:
            self._divoomBluetoothDevice.score_1 = self._attr_state
        elif self._num == 2:
            self._divoomBluetoothDevice.score_2 = self._attr_state
        self._divoomBluetoothDevice.updateScore()
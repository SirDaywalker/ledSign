__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

from network import WLAN, STA_IF
from time import sleep

WIFI_SETTINGS: dict = {
    "SSID": "Impfchip-6a29e5",
    "Password": "Schnitzel",
}


def connect_to_wifi() -> WLAN:
    global wifi
    wifi: WLAN = WLAN(STA_IF)
    wifi.active(True)
    wifi.disconnect()

    print("Trying to connect to wifi...", end="")
    wifi.connect(WIFI_SETTINGS["SSID"], WIFI_SETTINGS["Password"])

    while not wifi.status() == 3:
        print('.', end="")
        sleep(1)

    print('\n', f"\033[92mConnected successfully to Wifi! As: {wifi.ifconfig()[0]}\033[0m")
    return wifi


if __name__ == '__main__':
    print("Booting up...")
    connect_to_wifi()

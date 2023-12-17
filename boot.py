__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

from network import WLAN, STA_IF
from time import sleep

WIFI_SETTINGS: dict = {
    "SSID": "Impfchip-6a29e5",
    "Password": "Schnitzel",
}


def connect_to_wifi() -> WLAN:
    wifi: WLAN = WLAN(STA_IF)
    wifi.active(True)
    wifi.disconnect()
    
    wifi.connect(WIFI_SETTINGS["SSID"], WIFI_SETTINGS["Password"])
    
    max_wait = 10
    while max_wait > 0:
        if wifi.status() < 0 or wifi.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for connection...")
        sleep(1)

    if wifi.status() != 3:
        raise RuntimeError(f"\033[91mFailed to connect to WIFI. Timed out after 10 seconds\033[0m")

    print(f"\033[92mConnected successfully to Wifi! As: {wifi.ifconfig()[0]}\033[0m")
    return wifi


if __name__ == '__main__':
    print("Booting up...")
    connect_to_wifi()

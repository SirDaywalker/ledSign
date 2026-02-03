__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

from network import WLAN, STA_IF
from time import sleep

from settings import SETTINGS


def connect_to_wifi(ssid: str, psw: str) -> WLAN:
    """
    Connects to the Wi-Fi network.

    :param ssid: the Wi-Fi name.
    :param psw: the password of the network.
    :return: the new Wi-Fi-Object.
    """
    global wifi
    wifi: WLAN = WLAN(STA_IF)
    wifi.active(True)
    wifi.disconnect()

    print("Trying to connect to wifi...", end="")
    wifi.connect(ssid, psw)

    while not wifi.status() == 3:
        print('.', end="")
        sleep(1)

    print('\n', f"\033[92mConnected successfully to Wifi! As: {wifi.ifconfig()[0]}\033[0m")
    return wifi


if __name__ == '__main__':
    print("Booting up...")
    connect_to_wifi(SETTINGS["SSID"], SETTINGS["Password"])
    print("Starting webserver...")

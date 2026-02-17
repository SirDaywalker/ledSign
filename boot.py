__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

from network import WLAN, STA_IF
from time import sleep
from settings import SETTINGS


def connect_to_wifi(ssid: str, password: str) -> WLAN:
    """
    Connects to the Wi-Fi network.

    :param ssid: the Wi-Fi name.
    :param password: the password of the network.
    :return: the new Wi-Fi-Object.
    """
    wifi: WLAN = WLAN(STA_IF)
    wifi.active(True)
    wifi.disconnect()
    print("Trying to connect to Wi-Fi...", end="")
    try:
        wifi.connect(ssid, password)

        counter = 0
        while wifi.status() != 3:
            if counter == 5:
                wifi.disconnect()
                raise Exception("Couldn't connect to Wi-Fi! Please check your credentials or WiFi connection.")
            print('.', end="")
            counter += 1
            sleep(1)

        print('\n', f"  \033[92mConnected successfully to Wi-Fi! As: {wifi.ifconfig()[0]}\033[0m", sep="")
        return wifi

    except Exception as e:
        print('\n', f"  \033[91m{e}\033[0m", sep="")
        return wifi


print("Booting up...")
global_wifi = connect_to_wifi(SETTINGS["SSID"], SETTINGS["Password"])

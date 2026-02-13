__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

from network import WLAN, STA_IF
from time import sleep
from settings import SETTINGS
import uos


def get_current_version() -> str:
    """
    Retrieves the current version of the project from the "pyproject.toml" file.

    This function scans the "pyproject.toml" file to locate and extract the version
    information specified under the [project] section. If the file cannot be accessed
    or the version cannot be determined, it returns "unknown".

    Returns:
        str: The project version as a string if found; otherwise, "unknown".

    Raises:
        OSError: If there is an issue accessing the "pyproject.toml" file.
    """
    try:
        in_project_section = False

        with open("pyproject.toml", "r") as pyproject_file:
            for line in pyproject_file:
                line = line.strip()

                # Kommentare/Leerzeilen ignorieren
                if not line or line.startswith("#"):
                    continue

                # Section erkennen
                if line == "[project]":
                    in_project_section = True
                    continue

                # wenn neue Section anfängt -> project-section verlassen
                if line.startswith("[") and line.endswith("]") and line != "[project]":
                    in_project_section = False
                    continue

                # version innerhalb [project] suchen
                if in_project_section and line.startswith("version"):
                    # version = "0.1.0"
                    parts = line.split("=", 1)
                    version = parts[1].strip().strip('"')
                    return version

    except OSError:
        return "unknown"

    return "unknown"


def ensure_dir(path) -> None:
    """
    Ensures that a directory exists at the specified path. If the directory
    does not exist, it attempts to create it. If creation fails due to an
    OSError, the exception is silently ignored.

    Parameters:
    path (str): The path of the directory to verify or create.

    Returns:
    None
    """
    try:
        uos.mkdir(path)
        print(f"  Created directory: {path}")
    except OSError:
        pass


def generate_homepage_with_version() -> None:
    """
    Loads the HTML content of the homepage, inserts the current version into
    the predefined {{VERSION}} placeholder, and returns the processed HTML
    content. The current version is determined using the get_current_version
    function.

    Returns:
        str: The processed HTML content with the current version inserted into the
        {{VERSION}} placeholder.
    """
    print("Generating homepage with version...")
    with open("/lib/static/index.html", "r") as html_file:
        html = html_file.read()

    version = get_current_version()

    ensure_dir("/lib/generated")

    with open("/lib/generated/index_with_version.html", "w") as html_with_version_file:
        html_with_version_file.write(html.replace("{{VERSION}}", version))

    print("  ...Done")


def connect_to_wifi(ssid: str, password: str) -> WLAN:
    """
    Connects to the Wi-Fi network.

    :param ssid: the Wi-Fi name.
    :param password: the password of the network.
    :return: the new Wi-Fi-Object.
    """
    try:
        wifi: WLAN = WLAN(STA_IF)
        wifi.active(True)
        wifi.disconnect()

        print("Trying to connect to Wi-Fi...", end="")
        wifi.connect(ssid, password)

        counter = 0
        while wifi.status() != 3:
            if counter == 5:
                wifi.disconnect()
                raise Exception("Couldn't connect to Wi-Fi! Please check your credentials or WiFi connection.")
            print('.', end="")
            counter += 1
            sleep(1)

        print(f"\033[92mConnected successfully to Wi-Fi! As: {wifi.ifconfig()[0]}\033[0m")
        return wifi

    except Exception as e:
        print(f"\033[91m{e}\033[0m")
        return None


print("Booting up...")
global_wifi = connect_to_wifi(SETTINGS["SSID"], SETTINGS["Password"])
generate_homepage_with_version()

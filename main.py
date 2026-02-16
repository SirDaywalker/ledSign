__author__ = "Jannis Dickel"

from lib.leds import Leds
from lib.usSensor import UsSensor
from lib.microdot_asyncio import Microdot, send_file, Response, Request
from boot import global_wifi

import uasyncio as asyncio

from settings import SETTINGS

led: Leds = Leds(SETTINGS["NumLEDs"], SETTINGS["LEDPin"])
us_sensor: UsSensor = UsSensor(SETTINGS["TriggerPin"], SETTINGS["EchoPin"])
app: Microdot = Microdot()
current_task: asyncio.Task = None 

# This is still part of the Wi-Fi connection
try:
    if global_wifi.status() == 3:
        led.blink_up(target_color=led.GREEN)
    else:
        led.blink_up(sleep_time=0.2)
    if "StartColor" in SETTINGS:
        led.fade(SETTINGS["StartColor"])
except Exception as e:
    print(f"\033[91m{e}\033[0m")
    pass


def start_led_task(coro):
    """
    Beendet den aktuellen LED-Task sauber und startet einen neuen.
    Verhindert 'Task was destroyed but it is pending'.
    """
    global current_task

    if current_task and not current_task.done():
        current_task.cancel()

    current_task = asyncio.create_task(coro)


async def run_colors() -> None:
    """
    Measures the distance the sensor provides and changes the colors according to the distance.
    """
    while True:
        distance: int = int(us_sensor.read_distance())

        if distance <= 21:
            await kill_current_task(None)

        if distance < 3 and not led.color == led.OFF:
            led.blink_up()
            led.fade(led.OFF)

        elif 3 < distance < 6:
            led.fade(led.RED)

        elif 6 < distance < 9:
            led.fade(led.ORANGE)

        elif 9 < distance < 12:
            led.fade(led.YELLOW)

        elif 12 < distance < 15:
            led.fade(led.GREEN)

        elif 15 < distance < 18:
            led.fade(led.BLUE)

        elif 18 < distance < 21:
            led.fade(led.PURPLE)

        await asyncio.sleep(0.2)


def start_server() -> None:
    """
    Starts the Server.
    """
    try:
        app.run(port=80)
    except Exception as e:
        app.shutdown()
        print("Server shut down due to error:", e)


def get_current_version():
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


def load_homepage_with_version():
    """
    Loads the HTML content of the homepage, inserts the current version into
    the predefined {{VERSION}} placeholder, and returns the processed HTML
    content. The current version is determined using the get_current_version
    function.

    Returns:
        str: The processed HTML content with the current version inserted into the
        {{VERSION}} placeholder.
    """
    with open("/lib/static/index.html", "r") as html_file:
        html = html_file.read()

    version = get_current_version()
    html = html.replace("{{VERSION}}", version)

    return html


@app.before_request
async def kill_current_task(request: Request) -> None:
    """
    Cancels the current LED task before any new command.
    """
    global current_task

    if current_task and not current_task.done():
        current_task.cancel()
        try:
            await current_task 
        except asyncio.CancelledError:
            pass


@app.get("/")
def homepage(request: Request) -> Response:
    """
    Maps the homepage request and sends it to the user.
    :param request: the clients request (homepage call)
    :return: the index.html
    """
    return Response(load_homepage_with_version(), headers={"Content-Type": "text/html"})


@app.get("/favicon.png")
def get_favicon(request: Request) -> Response:
    """
    Maps the favicon request and sends it to the user.
    :param request: the clients request
    :return: the favicon.png
    """
    return send_file("/lib/static/favicon.png", content_type="image/png")


@app.get("/css/<path:path>")
def get_css(request: Request, path: str) -> Response:
    """
    Maps the css request and sends it to the user.
    :param request: the clients request
    :return: the css file
    """
    return send_file("/lib/static/" + path)


@app.get("/js/<path:path>")
def get_js(request: Request, path: str) -> Response:
    """
    Maps the js request and sends it to the user.
    :param request: the clients request
    :return: the css file
    """
    return send_file("/lib/static/" + path)


@app.put("/set-rgb-color")
def set_color(request: Request) -> (str, int):
    """
    Maps the rgb-color set and changes the color.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    try:
        data = request.json 
        led.set_all((
            int(data.get('r')),
            int(data.get('g')),
            int(data.get('b'))
        ))
    except (TypeError, ValueError):
        return "Non-fitting params", 400

    return "Changed color", 200


@app.put("/breath")
async def breath(request) -> (str, int):
    """
    Maps the "breath"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    try:
        data = request.json
        start_led_task(
            led.breath(
                (int(data.get('r')), int(data.get('g')), int(data.get('b'))),
                delay=int(data.get('delay'))
            )
        )
    except (TypeError, ValueError):
        return "Non-fitting params", 400

    return "Breathing now", 200


@app.put("/cycle")
async def cycle(request) -> (str, int):
    """
    Maps the "cycle"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    try:
        data = request.json
        start_led_task(
            led.cycle(
                (int(data.get('c1r')), int(data.get('c1g')), int(data.get('c1b'))),
                (int(data.get('c2r')), int(data.get('c2g')), int(data.get('c2b'))),
                delay=int(data.get('delay'))
            )
        )
    except (TypeError, ValueError):
        return "Non-fitting params", 400

    return "Cycling now", 200


@app.put("/candy-tornado")
async def candy_tornado(request) -> (str, int):
    """
    Maps the "CandyTornado"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    try:
        data = request.json
        start_led_task(
            led.candy_tornado(
                sat=int(data.get('sat')),
                val=int(data.get('val')),
                delay_ms=int(data.get('delay_ms')),
                hue_gap=int(data.get('hue_gap')),
                hue_cycle_speed=int(data.get('hue_cycle_speed'))
            )
        )
    except (TypeError, ValueError):
        return "Non-fitting params", 400

    return "Going wild", 200

@app.put("/lottery")
async def lottery(request) -> (str, int):
    try:
        data = request.json
        start_led_task(
            led.lottery(
                (int(data.get('mr')), int(data.get('mg')), int(data.get('mb'))),
                (int(data.get('br')), int(data.get('bg')), int(data.get('bb'))),
                int(data.get('delay'))
            )
        )
    except (TypeError, ValueError):
        return "Non-fitting params", 400

    return "Doing da thing", 200

print("Starting Ultrasound-Sensor...", end="")
asyncio.create_task(run_colors())
print("Done")
print("Starting webserver...")
start_server()

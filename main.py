__author__ = "Jannis Dickel"

from lib.leds import Leds
from lib.usSensor import UsSensor
from lib.microdot_asyncio import Microdot, send_file, Response, Request

import uasyncio as asyncio

from settings import SETTINGS

led: Leds = Leds(SETTINGS["AnzLEDs"], SETTINGS["LEDPin"])
us_sensor: UsSensor = UsSensor(SETTINGS["TriggerPin"], SETTINGS["EchoPin"])
app: Microdot = Microdot()
current_task: asyncio.Task = None 


try:
    if wifi.status() == 3:
        led.blink_up(led.GREEN)
except Exception:
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

        if distance < 3:
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
        print("Server successfully started")
        app.run(port=80)
    except Exception as e:
        print("Server shut down due to error:", e)
        app.shutdown()


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
    return send_file("/lib/static/index.html", content_type="text/html")


@app.get("/css/<path:path>")
def static(request: Request, path: str) -> Response:
    """
    Maps the css request and sends it to the user.
    :param request: the clients request
    :return: the css file
    """
    return send_file("/lib/static/" + path)


@app.get("/js/<path:path>")
def static(request: Request, path: str) -> Response:
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


asyncio.create_task(run_colors())
start_server()

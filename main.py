__author__ = "Jannis Dickel"

from lib.leds import Leds
from lib.usSensor import UsSensor
from lib.microdot_asyncio import Microdot, send_file, Response, Request

import uasyncio as asyncio

led: Leds = Leds(6, 20)
us_sensor: UsSensor = UsSensor(16, 17)
app: Microdot = Microdot()
current_task: asyncio.Task = None

global wifi
if wifi.status() == 3:
    led.blink_up(led.GREEN)


async def run_colors() -> None:
    """
    Measures the distance the sensor provides and changes the colors according to the distance.
    :return: None
    """
    while True:
        distance: int = int(us_sensor.read_distance())

        if distance <= 21:
            await kill_current_task("")

        if distance < 3:
            led.blink_up()
            led.fade(led.OFF)

        elif 3 < distance < 6:
            led.fade(led.RED)

        elif 6 < distance < 9:
            led.fade(led.YELLOW)

        elif 9 < distance < 12:
            led.fade(led.GREEN)

        elif 12 < distance < 15:
            led.fade(led.CYAN)

        elif 15 < distance < 18:
            led.fade(led.BLUE)

        elif 18 < distance < 21:
            led.fade(led.PURPLE)

        await asyncio.sleep(0.2)


def start_server() -> None:
    """
    Starts the Server.
    :return: None
    """
    try:
        print("Server successfully started")
        app.run(port=80)
    except:
        app.shutdown()
        print("Server shut down")


@app.before_request
async def kill_current_task(request: Request) -> None:
    """
    Cancels the current task before any mapping.
    :param request: the clients request
    :return: None
    """
    if current_task:
        current_task.cancel()


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
        led.set_all((
            int(request.json['r']),
            int(request.json['g']),
            int(request.json['b'])
        ))
    except ValueError:
        return "Non-fitting params", 400

    return "Changed color", 200


@app.put("/breath")
async def breath(request) -> (str, str):
    """
    Maps the "breath"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    global current_task
    try:
        current_task = asyncio.create_task(led.breath((
            int(request.json['r']),
            int(request.json['g']),
            int(request.json['b'])),
            delay=int(request.json['delay'])
        ))
    except TypeError or ValueError:
        return "Non-fitting params", 400

    return "Breathing now", 200


@app.put("/cycle")
async def cycle(request) -> (str, int):
    """
    Maps the "cycle"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    global current_task
    try:
        current_task = asyncio.create_task(led.cycle((
            int(request.json['c1r']),
            int(request.json['c1g']),
            int(request.json['c1b'])
        ), (
            int(request.json['c2r']),
            int(request.json['c2g']),
            int(request.json['c2b'])
        ),
            delay=int(request.json['delay'])
        ))
    except TypeError or ValueError:
        return "Non-fitting params", 400

    return "Cycling now", 200


@app.put("/candy-tornado")
async def candy_tornado(request) -> (str, int):
    """
    Maps the "CandyTornado"-command and changes the led-stripe behaviour.
    :param request: the clients request
    :return: a tuple containing the html-status text and code
    """
    global current_task
    try:
        current_task = asyncio.create_task(led.candy_tornado(
            sat=int(request.json['sat']),
            val=int(request.json['val']),
            delay_ms=int(request.json['delay_ms']),
            hue_gap=int(request.json['hue_gap']),
            hue_cycle_speed=int(request.json['hue_cycle_speed'])
        ))
    except TypeError or ValueError:
        return "Non-fitting params", 400

    return "Going wild", 200


asyncio.create_task(run_colors())
start_server()

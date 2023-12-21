__author__ = "Jannis Dickel"

from lib.leds import Leds
from lib.usSensor import UsSensor
from lib.microdot_asyncio import Microdot

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
    print("Starting webserver...")
    try:
        app.run(port=80)
    except:
        app.shutdown()


@app.before_request
async def kill_current_task(request) -> None:
    """
    Cancels the current task before any mapping.

    :param request: the clients request (Not interesting)
    :return: None
    """
    if current_task:
        current_task.cancel()


@app.get('/')
def homepage(request) -> (str, int, str):
    """
    Reads in the index.html and sends it to the user.

    :param request: the clients request (homepage call)
    :return: a tuple containing the page, the htmlstauts code and a json how to use the html.
    """

    with open("lib/templates/index.html") as index:
        index_html: str = index.read()

    return index_html, 200, {'Content-Type': 'text/html'}


@app.get("/set-rgb-color")
def set_color(request) -> (str, int):
    """
    Maps the rgb-color set.
    Mapping Pattern:  http://<ip addr>/change-color?r=[int]&g=[int]&b=[int]

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    try:
        led.set_all((
            int(request.args['r']),
            int(request.args['g']),
            int(request.args['b'])
        ))
    except ValueError:
        return "Non fitting params", 400

    return "Changed color", 200


@app.get("/set-hsv-color")
def fade_color(request) -> (str, int):
    """
    Maps the hsv-color set.
    Mapping Pattern: http://<ip addr>/change-color?h=[int]&s=[int]&v=[int]

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    try:
        led.set_all((
            led.convert_hsv_to_rgb(
                int(request.args['h']),
                int(request.args['s']),
                int(request.args['v'])
            )
        ))
    except ValueError:
        return "Non fitting params", 400

    return "Changed color", 200


@app.get("/fade-rgb-color")
def fade_color(request) -> (str, int):
    """
    Maps the fading to a rgb-color.
    Mapping Pattern: http://<ip addr>/fade-color?r=[int]&g=[int]&b=[int]

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    try:
        led.fade((
            int(request.args['r']),
            int(request.args['g']),
            int(request.args['b'])
        ))
    except ValueError:
        return "Non fitting params", 400

    return "Changed color", 200


@app.get("/fade-hsv-color")
def fade_color(request) -> (str, int):
    """
    Maps the fading to a hsv-color.
    Mapping Pattern: http://<ip addr>/fade-color?h=[int]&s=[int]&v=[int]

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    try:
        led.fade((
            led.convert_hsv_to_rgb(
                int(request.args['h']),
                int(request.args['s']),
                int(request.args['v'])
            )
        ))
    except ValueError:
        return "Non fitting params", 400

    return "Changed color", 200


@app.get("/breath")
async def breath(request) -> (str, str):
    """
    Maps the "breath"-command.
    Mapping Pattern: http://<ip addr>/breath?r=[int]&g=[int]&b=[int]&delay=[int]<delay optional>

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    global current_task
    try:
        current_task = asyncio.create_task(led.breath((
            int(request.args['r']),
            int(request.args['g']),
            int(request.args['b'])
        )))
    except TypeError or ValueError:
        return "Non fitting params", 400

    return "Breathing now", 200


@app.get("/candy-tornado")
async def candy_tornado(request) -> (str, int):
    """
    Maps the "CandyTornado"-command.
    Mapping Pattern:
        http://<ip addr>/candy-tornado?
        sat=[int]&val=[int]&delay_ms=[int]&hue_gap=[int]&hue_cycle_speed=[int]
        <all path variables optional>

    :param request: the clients request (See above: Mapping Pattern)
    :return: a tuple containing the htmlstauts text and code
    """
    args_dict = {}
    for key in request.args.keys():
        args_dict[key] = int(request.args[key])

    global current_task
    try:
        current_task = asyncio.create_task(led.candy_tornado(**args_dict))
    except TypeError or ValueError:
        return "Non fitting params", 400

    return "Going wild", 200


asyncio.create_task(run_colors())
start_server()

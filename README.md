# LED SIGN - Pico W Project

The LED Sign project is a Pico W project that uses an ultrasonic sensor to read the distance of the hand or an object and changes the color of the LED according to the distance. There is also an integrated web server with even more options.

## Installation

Download the source code from my [GitHub](https://github.com/SirDaywalker/ledSign) and drag the "boot.py", "main.py", "settings.py" and the entire lib directory to your Pico W.

## Setup 
Open “settings.py” and change the values in the SETTINGS dict to your corresponding values.
```python
SETTINGS: dict = {
    # WIFI
    "SSID": "Your WIFI Name",
    "Password": "Your WIFI password",

    # LEDs
    "AnzLEDs": 6,  # Number of LEDs
    "LEDPin": 28,  # The pin your LEDs are connected to
    # optional
    "StartColor": Leds.OFF,  # First Color of the Sign to start with, see ./lib/leds.py

    # UsSensor
    "TriggerPin": 16,  # The pin of the trigger of your ultrasound sensor
    "EchoPin": 17  # The pin of the echo of your ultrasound sensor
}
```

For optimal use of the webserver feature, make sure to give the Pico a static IP address.

## Usage

The 3rd party libary "Microdot" by [miguelgrinberg](https://github.com/miguelgrinberg/microdot) to create an easy REST-API and webserver on the microcontroller.

## Contributing

Contact one of the Collaborators if you have a feature request.

## Bug-Report

You encountered a bug? [Please let me know!](https://github.com/SirDaywalker)

## License

[MIT](LICENSE)

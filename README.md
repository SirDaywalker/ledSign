# LED SIGN - Pico W Project

The LED Sign project is a Pico W project that uses an ultrasonic sensor to read the distance of the hand or an object and changes the color of the LED according to the distance. There is also an integrated web server with even more options.

## Installation

Download the source code from my [GitHub](https://github.com/SirDaywalker/ledSign) and drag the "boot.py", "main.py" and the entire lib directory to your Pico W.

## Setup 
Open “boot.py” and change the values in the WIFI_SETTINGS dict to your password and SSID (WIFI-Name).
```python
WIFI_SETTINGS: dict = {
    "SSID": "Your WIFI Name",
    "Password": "Your password",
}
```
Make also sure to change the Pins of the LED and US-Sensor like this:
```python
led: Leds = Leds(*num leds on stripe*, *Pin on the board*)
us_sensor: UsSensor = UsSensor(*trigger_Pin on thr board*, *echo_Pin on thr board*)
```

For optimal use of the webserver feature, make sure to give the Pico a static IP address.

## Usage

The 3rd party libary "Microdot" by [miguelgrinberg](https://github.com/miguelgrinberg/microdot) to create an easy REST-API and webserver on the microcontroller.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Bug-Report

You encountered a bug? [Please let me know!](https://github.com/SirDaywalker)

## License

[MIT](https://choosealicense.com/licenses/mit/)

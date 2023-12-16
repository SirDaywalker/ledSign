__author__ = "Jannis Dickel"

from machine import Pin
import time


class UsSensor:
    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        self.trigger: Pin = Pin(trigger_pin, Pin.OUT)
        self.echo: Pin = Pin(echo_pin, Pin.IN)

    def read_distance(self) -> float:
        # get distance
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(5)
        self.trigger.low()
        # get time
        while self.echo.value() == 0:
            signal_off = time.ticks_us()
        while self.echo.value() == 1:
            signal_on = time.ticks_us()

        return (signal_on - signal_off) * 0.03432 / 2

    @staticmethod
    def run_colors(us_sensor, led):
        while True:
            distance: int = int(us_sensor.read_distance())

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

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

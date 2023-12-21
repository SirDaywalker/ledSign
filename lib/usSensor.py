__author__ = "Jannis Dickel"

from machine import Pin
import time


class UsSensor:
    """
    Represents a hc-sr04 ultrasonic sensor.
    """

    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        """
        Constructs the UsSensor with given params.

        :param trigger_pin: the number of the trigger pin on board.
        :param echo_pin: the number of the echo pin on board.
        :return: None
        """
        self.trigger: Pin = Pin(trigger_pin, Pin.OUT)
        self.echo: Pin = Pin(echo_pin, Pin.IN)

    def read_distance(self) -> float:
        """
        Reads in the measured distance from the sensor.

        :return: the measured distance as float.
        """
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

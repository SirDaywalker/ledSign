__author__ = "Jannis Dickel"

from machine import Pin
import time

class Us_sensor:
    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)


    def read_distance(self) -> float:
        # get distance
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(5)
        self.trigger.low()
        # get time
        while self.echo.value() == 0:
           signaloff = time.ticks_us()
        while self.echo.value() == 1:         
           signalon = time.ticks_us()
    

        return (signalon - signaloff) * 0.03432 / 2
            
            
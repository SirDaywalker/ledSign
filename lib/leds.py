__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

import machine
import neopixel
import uasyncio
from time import sleep


class Leds:
    """
    An object that represents an LED-strip with individually controllable LEDs.
    """
    # initialization of all colors as statics
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    OFF = (0, 0, 0)

    def __init__(self, num_leds: int, pin: int) -> None:
        """
        Constructs a Led-Stripe-Object.

        :param num_leds: an int with the count of the LEDs in the Stripe
        :param pin: an int which represents the Pin on the ESP32
        """

        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_leds)
        self.color = self.OFF

    @staticmethod
    def convert_hsv_to_rgb(hue, sat, val) -> (int, int, int):
        """
        Takes a hsv value and converts it to a rgb value.

        :param hue: h (hue) of the hsv value
        :param sat: s (saturation) of the hsv value
        :param val: v (value) of the hsv value
        :return:
        """
        if hue >= 65536:
            hue %= 65536

        hue = (hue * 1530 + 32768) // 65536
        if hue < 510:
            b = 0
            if hue < 255:
                r = 255
                g = hue
            else:
                r = 510 - hue
                g = 255

        elif hue < 1020:
            r = 0
            if hue < 765:
                g = 255
                b = hue - 510
            else:
                g = 1020 - hue
                b = 255

        elif hue < 1530:
            g = 0
            if hue < 1275:
                r = hue - 1020
                b = 255
            else:
                r = 255
                b = 1530 - hue

        else:
            r = 255
            g = 0
            b = 0

        v1 = 1 + val
        s1 = 1 + sat
        s2 = 255 - sat

        r = ((((r * s1) >> 8) + s2) * v1) >> 8
        g = ((((g * s1) >> 8) + s2) * v1) >> 8
        b = ((((b * s1) >> 8) + s2) * v1) >> 8
        return r, g, b

    def set_all(self, color: (int, int, int)) -> None:
        """
        Sets all LEDs to the given color.

        :param color: the color to set to
        :return: None
        """

        for led in range(self.num_leds):
            self.np[led] = color
            self.color = color
        self.np.write()

    def fade(self, target_color: (int, int, int)) -> None:
        """
        Uses iteration to fade to the target_color.
        
        :param target_color: the color to fade to
        :return: None
        """
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]
          
        while self.color != target_color:
            if r < target_color[0]:
                r = r + 1
            if r > target_color[0]:
                r = r - 1
                 
            if g < target_color[1]:
                g = g + 1
            if g > target_color[1]:
                g = g - 1
                  
            if b < target_color[2]:
                b = b + 1
            if b > target_color[2]:
                b = b - 1
                
            self.set_all((r, g, b))

    def blink_up(self, target_color: (int, int, int) = RED) -> None:
        """
        Blinks-up 2 times in the given color. Red by default.
        :return: None
        """
        for i in range(2):
            self.set_all(target_color)
            sleep(0.5)
            self.set_all(self.OFF)
            sleep(0.5)

    async def candy_tornado(self, sat=255, val=255, delay_ms=10, hue_gap=65535, hue_cycle_speed=65535) -> None:
        """
        Runs an infinite tornado throughout all hsv-colors.
        The longer the stripe the better it will look.

        :param sat: Hue of hsv.
        :param val: Value of hsv.
        :param delay_ms: The delay between the single cycles.
        :param hue_gap: The gap between the colors. The smaller the gap the smoother it gets.
        :param hue_cycle_speed: The speed the colors cycle.
        :return: None
        """
        sync_hue = 0
        self.color = (0, 0, 0)

        while True:
            hue = sync_hue
            for i in range(self.num_leds):
                self.np[i] = self.convert_hsv_to_rgb(hue, sat, val)
                hue = (hue + (hue_gap // self.num_leds)) % 65536

            sync_hue = (sync_hue + (hue_cycle_speed // self.num_leds)) % 65536

            self.np.write()
            await uasyncio.sleep(delay_ms / 100)

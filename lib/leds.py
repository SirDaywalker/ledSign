__author__ = "Jannis Dickel"
__credits__ = ["Leon Reusch", "Jonas Witte"]

import machine
import neopixel
import uasyncio as asyncio
from time import sleep


class Leds:
    """
    Represents an LED-strip with a length of x individual individually controllable LEDs.
    """
    RED = (255, 0, 0)
    ORANGE = (255, 30, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    OFF = (0, 0, 0)

    def __init__(self, num_leds: int, pin: int) -> None:
        """
        Constructs a Led-Stripe-Object.

        :param num_leds: an int with the count of the LEDs in the Stripe.
        :param pin: an int which represents the Pin on the Board.
        :return: None.
        """
        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_leds)
        self.color = self.OFF

    @staticmethod
    def convert_hsv_to_rgb(hue, sat, val) -> tuple[int, int, int]:
        """
        Takes a hsv value and converts it to a rgb value.

        :param hue: h (hue) of the hsv value
        :param sat: s (saturation) of the hsv value
        :param val: v (value) of the hsv value
        :return: a tuple (r, g, b)
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

    @staticmethod
    def rgb_to_hsv(r, g, b):
        """
        Takes a rgb value and converts it to the hsv value.
        """
        r_, g_, b_ = r / 255, g / 255, b / 255
        mx = max(r_, g_, b_)
        mn = min(r_, g_, b_)
        diff = mx - mn

        if diff == 0:
            h = 0
        elif mx == r_:
            h = (60 * ((g_ - b_) / diff)) % 360
        elif mx == g_:
            h = (60 * ((b_ - r_) / diff)) + 120
        else:
            h = (60 * ((r_ - g_) / diff)) + 240

        h = int(h / 360 * 65535)

        s = 0 if mx == 0 else diff / mx
        s = int(s * 255)

        v = int(mx * 255)

        return h, s, v

    def set_all(self, color: tuple[int, int, int]) -> None:
        """
        Sets all LEDs to the given color.

        :param color: the color to set to.
        :return: None
        """
        for led in range(self.num_leds):
            self.np[led] = color
            self.color = color
        self.np.write()

    def fade(self, target_color: tuple[int, int, int]) -> None:
        """
        Uses iteration to fade to the target_color.

        :param target_color: the color to fade to.
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

    async def fade_hsv(self, h1, h2, s, v, delay):
        hue = h1

        diff = (h2 - h1) % 65536
        step = 1 if diff < 32768 else -1

        while hue != h2:
            hue = (hue + step) % 65536
            rgb = self.convert_hsv_to_rgb(hue, s, v)
            self.set_all(rgb)
            await asyncio.sleep_ms(delay)

    def blink_up(self, target_color: tuple[int, int, int] = RED) -> None:
        """
        Blinks-up 2 times in the given color. Red by default.
        :param target_color: the to set to.
        :return: None
        """
        for i in range(2):
            self.fade(target_color)
            sleep(0.5)
            self.fade(self.OFF)
            sleep(0.5)

    async def breath(self, target_color: tuple[int, int, int], delay: int = 10) -> None:
        """
        Blinks up the color continuously.

        :param target_color: The color to blink up.
        :param delay: the speed it blinks up. 10ms by default.
        :return: None
        """

        rgb = (0, 0, 0)
        self.color = rgb
        while True:
            while rgb != target_color:
                rgb = tuple([rgb[i] + 1 if rgb[i] < target_color[i] else rgb[i] for i in range(3)])
                self.set_all(rgb)
                await asyncio.sleep_ms(delay)

            while rgb != (0, 0, 0):
                rgb = tuple([rgb[i] - 1 if rgb[i] > 0 else rgb[i] for i in range(3)])
                self.set_all(rgb)
                await asyncio.sleep_ms(delay)

    async def cycle(self, target1: tuple[int, int, int], target2: tuple[int, int, int], delay: int = 10) -> None:
        if target1 == target2:
            raise ValueError("Colors must differ")
        
        delay = int(delay / 100)

        h1, s1, v1 = self.rgb_to_hsv(*target1)
        h2, s2, v2 = self.rgb_to_hsv(*target2)

        s = max(s1, s2)
        v = max(v1, v2)

        while True:
            await self.fade_hsv(h1, h2, s, v, delay)
            await self.fade_hsv(h2, h1, s, v, delay)

    async def candy_tornado(self, sat=255, val=255, delay_ms=10, hue_gap=36358, hue_cycle_speed=4885) -> None:
        """
        Runs an infinite tornado of candies throughout all hsv-colors.
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
            self.color = self.np[0]
            await asyncio.sleep(delay_ms / 100)

    async def lottery(self, main: tuple[int, int, int], balls: tuple[int, int, int], delay_ms=100) -> None:
         while True: 
            for i in range(self.num_leds):
                self.set_all(main)
                self.np[i] = balls 
                self.np[self.num_leds - 1 - i] = balls
                self.np.write()
                await asyncio.sleep_ms(delay_ms)

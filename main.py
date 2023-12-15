__author__ = "Jannis Dickel"

from lib.leds import Leds
from lib.usSensor import UsSensor
from time import sleep


def main() -> None:   
    led: Leds = Leds(6, 20)
    led.set_all(led.OFF)
    us_sensor: UsSensor = UsSensor(16, 17)

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
            
        else:
            pass
        
        sleep(0.5)

    
if __name__ == '__main__':
    main()

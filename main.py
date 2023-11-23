from lib.leds import Leds
from lib.us_sensor import Us_sensor
import time


def main() -> None:   
    led = Leds(6, 20)
    led.set_all(led.OFF)
    us_sensor = Us_sensor(16, 17)
    while True:
        us_sensor.run()
    
    
if __name__ == '__main__':
    main()

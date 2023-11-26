from machine import Pin
import time

class Us_sensor:
    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
    
#    def read_distance():
 #       trigger.low()
  #      sleep_us(2)
   #     trigger.high()
    #    sleep_us(5)
     #   trigger.low()
        

    def run(self):
        while True:
            # Abstand messen
            self.trigger.low()
            time.sleep_us(2)
            self.trigger.high()
            time.sleep_us(5)
            self.trigger.low()
            # Zeitmessungen
            while self.echo.value() == 0:
               signaloff = time.ticks_us()
            while self.echo.value() == 1:         
               signalon = time.ticks_us()
            # Vergangene Zeit ermitteln
            timepassed = signalon - signaloff
            # Abstand/Entfernung ermitteln
            # Entfernung über die Schallgeschwindigkeit (34320 cm/s bei 20 °C) berechnen
            # Durch 2 teilen, wegen Hin- und Rückweg
            abstand = timepassed * 0.03432 / 2
            # Ergebnis ausgeben
            print('    Off:', signaloff)
            print('     On:', signalon)
            print('   Zeit:', timepassed)
            print('Abstand:', str("%.2f" % abstand), 'cm', "\n")
            # 3 Sekunde warten
            time.sleep(3)
            
            
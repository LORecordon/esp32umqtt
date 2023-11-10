import time
from machine import Pin, PWM
               
class SensorMagnetico:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN,Pin.PULL_UP)
    
    def leer_sensor(self):
        estado = self.pin.value()
        time.sleep(0.25)
        if estado == 0:
            print("Locker cerrado")
            return 0
        else:
            print("Locker abierto")
            return 1
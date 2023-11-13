from machine import Pin,PWM
import time

class Servo:
    def __init__(self, pin):
        self.pin = PWM(Pin(pin,mode=Pin.OUT))
        self.pin.freq(50)
        self.state = True
    
    def levantar(self):
        self.pin.duty(110)
        time.sleep(1)
        self.pin.duty(0)
        self.state = True
    
    def bajar(self):
        self.pin.duty(40)
        time.sleep(1)
        self.pin.duty(0)
        self.state = False
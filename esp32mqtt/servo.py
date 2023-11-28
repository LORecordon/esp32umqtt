from machine import Pin,PWM
import time

class Servo:
    def __init__(self, pin, inverse=False):
        self.pin = PWM(Pin(pin,mode=Pin.OUT))
        self.pin.freq(50)
        self.state = True
        self.inverse = inverse
    
    def levantar(self):
        if self.inverse:
            self.pin.duty(40)
            time.sleep(1)
            self.pin.duty(0)
            self.state = True
            return
        self.pin.duty(110)
        time.sleep(1)
        self.pin.duty(0)
        self.state = True
    
    def bajar(self):
        if self.inverse:
            self.pin.duty(110)
            time.sleep(1)
            self.pin.duty(0)
            self.state = False
            return
        self.pin.duty(40)
        time.sleep(1)
        self.pin.duty(0)
        self.state = False
import time
from machine import Pin, PWM


class SensorInfrarrojo:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)
    
    def leer_sensor(self):
        estado = self.pin.value()
        time.sleep(0.25)
        if estado == 0:
            print("Objeto detectado cerca del sensor")
            return 0
        else:
            print("No se detecta ningún objeto cerca del sensor")
            return 1


#infrarrojo_1 = SensorInfrarrojo(19)
#resultado = infrarrojo_1.leer_sensor()
#print("Resultado:", resultado)
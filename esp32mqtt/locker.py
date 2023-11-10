from machine import Pin, PWM
from ir import SensorInfrarrojo
from mag import SensorMagnetico
from servo import Servo
import time

class Locker:
    def __init__(self, nickname, height, width, length, servoPin, irPin, magPin, ledPin):
        self.nickname = nickname
        self.state = 0
        self.servo = Servo(servoPin)
        self.ir = SensorInfrarrojo(irPin)
        self.mag = SensorMagnetico(magPin)
        self.led = Pin(ledPin, Pin.OUT)
        self.height = height
        self.width = width
        self.length = length
        self.led.value(0)



    def deteccion_closed(self, sensor):
        tiempo = 20
        for i in range(tiempo):
            if sensor.leer_sensor() == 1:
                return True
            else:
                time.sleep(1)
        return False

    def deteccion_open(self, sensor):
        tiempo = 20
        for i in range(tiempo):
            if sensor.leer_sensor() == 0:
                return True
            else:
                time.sleep(1)
        return False

    def operator_load(self):
        self.state = 2
        self.servo.levantar()
        print("Reading Mag Sensor")
        magvalue = self.deteccion_closed(self.mag)
        if not magvalue:
            print("Locker not opened")
            self.state = 1
            self.servo.bajar()
            #send message
            return False
        irvalue = self.deteccion_open(self.ir)
        if irvalue:
            print("Locker Loaded")
            self.state = 3
        else: 
            print("Locker not loaded")
            self.state = 1
        time.sleep(2)
        magvalue = self.deteccion_open(self.mag)
        if magvalue:
            print("Closing Locker")
            time.sleep(1)
            self.servo.bajar()
        else:
            print("Locker not closed")

    def client_unload(self):
        self.state = 4
        self.servo.levantar()
        print("Reading Mag Sensor")
        magvalue = self.deteccion_closed(self.mag)
        if not magvalue:
            print("Locker not opened")
            self.state = 3
            self.servo.bajar()
            #send message
            return False
        print("Reading IR Sensor")
        irvalue = self.deteccion_closed(self.ir)
        if irvalue:
            print("Locker Unloaded")
            self.state = 0
        else: 
            print("Locker not unloaded")
            self.state = 3

        time.sleep(2)
        print("Reading Mag Sensor")
        magvalue = self.deteccion_open(self.mag)
        if magvalue:
            print("Closing Locker")
            time.sleep(1)
            self.servo.bajar()
        else:
            print("Locker not closed")

    
    def status(self):
        if self.ir.leer_sensor() == 0:
            isem = False
        else:
            isem = True


        mydata = {
            "nickname": self.nickname,
            "state": self.state,
            "is_open": self.servo.state,
            "is_empty": isem
        }
        return mydata

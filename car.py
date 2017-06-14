from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# recommended for auto-disabling motors on shutdown!
mh = Adafruit_MotorHAT(addr=0x60)
def powerOff():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)# atexit.register(car.powerOff)
class Car(object):
    """docstring for ClassName"""
    # create a default object, no changes to I2C address or frequency
   
    def __init__ (self):
        super(Car, self).__init__()
        self._wheels = [ mh.getMotor(1), mh.getMotor(2), mh.getMotor(3), mh.getMotor(4) ]
        self._speed = 10

    def moveForward (self):
        for wheel in self._wheels:
            wheel.run(Adafruit_MotorHAT.FORWARD)

    def moveBackward (self):
        for wheel in self._wheels:
            wheel.run(Adafruit_MotorHAT.BACKWARD)
   
    def accelerate (self):
        for wheel in self._wheels:
            wheel.setSpeed(self._speed)

    def stop (self):
        for i in range(255, 0, -10):
            for wheel in self._wheels:
                wheel.setSpeed(i)

    def right(self):
        self._wheels[2].setSpeed(self.speed)
        self._wheels[3].setSpeed(self.speed)
        self._wheels[0].setSpeed(self.speed / 2)
        self._wheels[1].setSpeed(self.speed / 2)

    def left(self):
        self._wheels[0].setSpeed(self.speed)
        self._wheels[1].setSpeed(self.speed)
        self._wheels[2].setSpeed(self.speed / 2)
        self._wheels[3].setSpeed(self.speed / 2)

    def spin(self):
        self._wheels[2].setSpeed(self.speed)
        self._wheels[3].setSpeed(self.speed)
        self._wheels[0].setSpeed(self.speed / 2)
        self._wheels[1].setSpeed(self.speed / 2)


    @property
    def speed (self):
        return self._speed

    @speed.setter
    def speed (self , speed):
        self._speed = speed

    def powerOff(self):
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def __del__(self):
        self.powerOff()


if __name__ == '__main__':
    i = 0
    car = Car()
    car.speed = 100
    car.moveForward()
    while 1:
        try:          
            car.turnRight()
        except KeyboardInterrupt:
            car.powerOff()
            atexit.register(car.powerOff)
            raise


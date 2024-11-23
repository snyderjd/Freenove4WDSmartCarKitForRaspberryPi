import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685

class UltrasonicTwo:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        self.MAX_DISTANCE = 300 # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE * 60 # calculate timeout according to the maximum measuring distance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def pulseIn(self, pin, level, timeOut):
        # obtain pulse time of a pin under timeout
        t0 = time.time()
        while (GPIO.input(pin) != level):
            if ((time.time() - t0) > timeOut * 0.000001):
                return 0;
        t0 = time.time()
        while (GPIO.input(pin) == level):
            if ((time.time() - t0) > timeOut * 0.000001):
                return 0;
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime

    def get_distance(self):
        # get the measurement results of ultrasonic module, with unit: cm
        distance_cm = [0, 0, 0, 0, 0]
        for i in range(5):
            # make trigger_pin output 10us HIGH level
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001) # 10us
            # make trigger_pin output LOW level
            GPIO.output(self.trigger_pin, GPIO.LOW)
            # read pulse time of echo_pin
            pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, self.timeOut)
            # calculate distance with sound speed 340m/s
            distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0
        distance_cm = sorted(distance_cm)
        return int(distance_cm[2])
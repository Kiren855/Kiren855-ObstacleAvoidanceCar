import RPi.GPIO as GPIO
import time

class Movement:
    def __init__(self, in1_pin=17, in2_pin=27, in3_pin=23, in4_pin=24):

        GPIO.setmode(GPIO.BCM)
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.in3_pin = in3_pin
        self.in4_pin = in4_pin

        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.in3_pin, GPIO.OUT)
        GPIO.setup(self.in4_pin, GPIO.OUT)

    def turn_right(self, st=0):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.LOW)
        time.sleep(st)


    def turn_left(self, st=0):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.HIGH)   
        time.sleep(st)

    def move_forward(self, st=0):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.LOW)
        time.sleep(st)

    def move_backward(self, st=0):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.HIGH)
        time.sleep(st)

    
    def turn_left_by_angle(self, angle=0):
        st = angle / 180 * 0.80
        print("time ", st)
        self.turn_left(st)
    
    def turn_right_by_angle(self, angle=0):
        st = angle / 180 * 0.80
        print("time ", st)
        self.turn_right(st)
        
    
    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()



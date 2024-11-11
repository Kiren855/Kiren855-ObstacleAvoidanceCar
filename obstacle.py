import RPi.GPIO as GPIO
import time


class UltrasonicSensor:
    def __init__(self, trigger_pin=5, echo_pin=6):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trigger_pin, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self.trigger_pin, GPIO.LOW)

        pulse_start, pulse_end = 0, 0

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return distance

    def cleanup(self):
        GPIO.cleanup()


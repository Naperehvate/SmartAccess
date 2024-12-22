from gpio_manager import GPIO
import time

class BuzzerController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def beep(self, duration=0.5):
        """Издаёт звуковой сигнал на указанное время."""
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)

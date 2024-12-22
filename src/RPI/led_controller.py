from gpio_manager import GPIO
import time

class LEDController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def blink(self, duration=0.5):
        """Мигание светодиода в течение указанного времени."""
        self.turn_on()
        time.sleep(duration)
        self.turn_off()

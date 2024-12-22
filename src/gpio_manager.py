import sys

if sys.platform == "win32":
    from Win.gpio_emulator import GPIO  # Используем эмулятор для Windows
else:
    print("Запуск на Raspberry Pi — использование реальных GPIO.")
    import RPi.GPIO as GPIO

# Инициализация GPIO
def initialize_gpio():
    GPIO.setmode(GPIO.BCM)

def cleanup_gpio():
    """Очистка GPIO перед завершением работы."""
    GPIO.cleanup()

    #GPIO.setwarnings(False)  # Отключаем предупреждения для Raspberry Pi

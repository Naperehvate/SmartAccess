import sys
import time
from gpio_manager import GPIO

# Импорт класса SimpleMFRC522
if sys.platform == "win32":
    from Win.rfid_simulator import SimpleMFRC522
else:
    from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# Обновлённый метод чтения карты
def read_card():
    try:
        print("Приложите карту к считывателю...")
        start_time = time.time()
        card_id, text = reader.read()
        duration = time.time() - start_time
        return card_id, text, duration
    except Exception as e:
        print(f"Ошибка при чтении карты: {e}")
        return None, None, 0
    finally:
        GPIO.cleanup()

# Обновлённый метод записи данных на карту
def write_card(data):
    try:
        print("Приложите карту для записи...")
        reader.write(data)
        print("Данные записаны.")
    except Exception as e:
        print(f"Ошибка при записи данных: {e}")
    finally:
        GPIO.cleanup()

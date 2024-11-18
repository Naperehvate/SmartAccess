import sys
from gpio_manager import GPIO

if sys.platform == "win32":
    print("Эмуляция RFID на Windows.")

    class SimpleMFRC522:
        @staticmethod
        def read():
            print("Симуляция чтения карты. Возвращается ID 123456789 и текст 'TestUser'.")
            return 123456789, "TestUser"

        @staticmethod
        def write(data):
            print(f"Симуляция записи данных: {data}")

else:
    print("Использование реального считывателя RFID на Raspberry Pi.")
    from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_card():
    """Чтение данных с карты"""
    try:
        print("Приложите карту к считывателю...")
        card_id, text = reader.read()
        return card_id, text
    except Exception as e:
        print(f"Ошибка при чтении карты: {e}")
        return None, None
    finally:
        GPIO.cleanup()

def write_card(data):
    """Запись данных на карту"""
    try:
        print("Приложите карту для записи...")
        reader.write(data)
        print("Данные записаны.")
    except Exception as e:
        print(f"Ошибка при записи данных: {e}")
    finally:
        GPIO.cleanup()

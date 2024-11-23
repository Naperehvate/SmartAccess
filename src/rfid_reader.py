import sys
from gpio_manager import GPIO

if sys.platform == "win32":
    print("Эмуляция RFID на Windows.")

    class SimpleMFRC522:
        cards = [
            (123456789, "AdminCard"),
            (987654321, "UserCard"),
            (111222333, "GuestCard")
        ]
        card_index = 0

        @staticmethod
        def read():
            card = SimpleMFRC522.cards[SimpleMFRC522.card_index]
            SimpleMFRC522.card_index = (SimpleMFRC522.card_index + 1) % len(SimpleMFRC522.cards)
            print(f"Симуляция чтения карты. Возвращается ID {card[0]} и текст '{card[1]}'.")
            return card[0], card[1]

        @staticmethod
        def write(data):
            print(f"Симуляция записи данных: {data}")

else:
    print("Использование реального считывателя RFID на Raspberry Pi.")
    from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_card():
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
    try:
        print("Приложите карту для записи...")
        reader.write(data)
        print("Данные записаны.")
    except Exception as e:
        print(f"Ошибка при записи данных: {e}")
    finally:
        GPIO.cleanup()

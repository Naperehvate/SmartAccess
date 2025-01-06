import sys
import time
from gpio_manager import GPIO

# Импорт класса SimpleMFRC522
if sys.platform == "win32":
    from Win.rfid_simulator import SimpleMFRC522
else:
    from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
my_list_card = []
temp_card = None

# Чтение карты
def read_card():
    global temp_card
    try:
        print("Считывание карты. Поднесите карту к считывателю...")
        card_id, text = reader.read()
        if temp_card == card_id:
            if len(my_list_card) < 3:
                my_list_card.append(card_id)
            card_id, text = reader.read()
        else:
            my_list_card.clear()
        temp_card = card_id
        attach_card = len(my_list_card)
        print (f"ID карты: {card_id} Текст: {text} Приложили эту карту: {attach_card + 1}")
        time.sleep(1)
        return card_id, text, attach_card
    except Exception as e:
        print(f"Ошибка при чтении карты: {e}")
        return None, None, 0
    finally:
        pass


def get_card_id_RFID():
    try:
        card_id, text = reader.read()
        return card_id
    except Exception as e:
        print(f"Ошибка при чтении карты: {e}")
        return None
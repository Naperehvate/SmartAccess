
from rfid_reader import read_card
from RPI.access_control import process_access
from gpio_manager import cleanup_gpio

def run_operational_mode():
    print("Запуск в рабочем режиме. Ctrl+C для выхода.")
    try:
        while True:
            card_id, text, attach_card = read_card()
            if card_id:
                process_access(card_id, attach_card)
            else:
                print("Не удалось считать карту.")
    except KeyboardInterrupt:
        print("\nВыход из системы.")
    finally:
        cleanup_gpio()

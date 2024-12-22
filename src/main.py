
import sys
import os 
sys.path.append(os.path.dirname(__file__))
from Win.admin_menu import *
from rfid_reader import *
from DB.database_manager import *
from gpio_manager import *

def main():
    create_database()
    set_setting("door_open_time", 3)  # Устанавливаем время открытия двери по умолчанию
    try:
        if sys.platform == "win32":
            print("Эмуляция на Windows. Запуск админ-меню.")
            admin_menu()
        else:
            print("Запуск в рабочем режиме. Нажмите Ctrl+C для выхода.")
            while True:
                card_id, _, duration = read_card()
                if card_id:
                    print(f"Считан ID карты: {card_id}, время прикладывания: {duration:.2f} сек.")
                    user = check_access(card_id)
                    if user:
                        name, access_level = user
                        if access_level == 2 and duration >= 3:
                            print("Переход в режим добавления пользователей.")
                            log_event("ModeSwitch", "Вход в режим добавления пользователей")
                        else:
                            print(f"Доступ предоставлен: {name}.")
                            open_door(get_setting("door_open_time", 3))
                            indicate_access_granted()
                    else:
                        print("Доступ запрещён. Пользователь не найден.")
                        indicate_access_denied()
                else:
                    print("Не удалось считать карту.")
    except KeyboardInterrupt:
        print("\nВыход из системы.")
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    main()

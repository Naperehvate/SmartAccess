
from DB.database_manager import check_access, get_setting
from RPI.access_manager import *

def process_access(card_id, duration):
    print(f"Считан ID карты: {card_id}, время прикладывания: {duration:.2f} сек.")
    user = check_access(card_id)
    if user:
        name, access_level = user
        if access_level == 2 and duration >= 3:
            print("Переход в режим добавления пользователей.")
            # Реализовать логику добавления пользователей
        else:
            print(f"Доступ предоставлен: {name}.")
            open_door(get_setting("door_open_time", 3))
            indicate_access_granted()
    else:
        print("Доступ запрещён. Пользователь не найден.")
        indicate_access_denied()

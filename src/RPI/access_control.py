import time
from DB.database_manager import *
from RPI.access_manager import *
from rfid_reader import *

# Константы уровней доступа
ACCESS_LEVEL_USER = 1
ACCESS_LEVEL_ADMIN = 2
ACCESS_LEVEL_SUPER_ADMIN = 3

def process_access(card_id, attach_card):
    print(f"Проверка ID карты в БД: {card_id}")
    user = check_access(card_id)
    
    if not user:
        print("Доступ запрещён. Пользователь не найден.")
        indicate_access_denied()
        return

    name, access_level = user

    if attach_card == 0:
        access_granted(name, card_id, access_level)
    elif attach_card == 1:
        handle_add_user_mode(card_id, access_level)
    elif attach_card == 2:
        handle_delete_user_mode(card_id, access_level)
    elif attach_card == 3:
        handle_open_access_mode(card_id, access_level)
    else:
        print("Доступ запрещён. Пользователь не найден. Карта не распознана.")
        indicate_access_denied()

def handle_add_user_mode(card_id, access_level):
    if access_level < ACCESS_LEVEL_ADMIN:
        access_granted(name, card_id, access_level)
        return

    print("Переход в режим добавления пользователей.")
    if not check_time_interval():
        print("Добавление пользователей отменено. Приложена другая карта.")
        indicate_access_denied()
        return

    print("Начало добавления пользователей. Для выхода приложите карту уровня 2 и выше.")
    while True:
        time.sleep(2)
        new_card_id = get_card_id_RFID()
        user = check_access(new_card_id)
        
        if user:
            name, new_access_level = user
            if new_access_level >= ACCESS_LEVEL_ADMIN:
                print("Добавление пользователей завершено. Пользователи добавлены.")
                indicate_access_granted()
                break
            else:
                print(f"Пользователь с ID карты {new_card_id} уже существует.\nОн имеет уровень доступа {new_access_level}.\nДобавление отменено.")
                indicate_access_denied()
        else:
            add_user(new_card_id, new_card_id, ACCESS_LEVEL_USER)
            print(f"Пользователь {new_card_id} успешно добавлен.")

def handle_delete_user_mode(card_id, access_level):
    if access_level < ACCESS_LEVEL_SUPER_ADMIN:
        access_granted(name, card_id, access_level)
        return

    print("Переход в режим удаления пользователей.")
    if not check_time_interval():
        print("Удаление пользователей отменено. Приложена другая карта.")
        indicate_access_denied()
        return

    print("Начало удаления пользователей. Для выхода приложите карту уровня 3.")
    while True:
        time.sleep(2)
        temp_card = get_card_id_RFID()
        user = check_access(temp_card)
        
        if user:
            name, temp_access_level = user
            if temp_access_level == ACCESS_LEVEL_SUPER_ADMIN:
                print("Удаление пользователей завершено. Пользователи удалены, переход в штатный режим.")
                indicate_access_granted()
                break
            else:
                delete_user(temp_card)
                print(f"Пользователь {temp_card} успешно удалён.")
                indicate_access_granted()
        else:
            print(f"Пользователь с ID карты {temp_card} не найден. Удаление отменено.")
            indicate_access_denied()

def handle_open_access_mode(card_id, access_level):
    if access_level < ACCESS_LEVEL_SUPER_ADMIN:
        access_granted(name, card_id, access_level)
        return

    print("Переход в режим открытого доступа и добавления пользователей.")
    if not check_time_interval():
        print("Режим открытого доступа отменён. Приложена другая карта или превышено время ожидания.")
        indicate_access_denied()
        return

    print("Включение режима. Для выхода приложите любую карту уровня 3.")
    while True:
        time.sleep(2)
        temp_card = get_card_id_RFID()
        user = check_access(temp_card)

        if user is None:
            if add_user(temp_card, temp_card, ACCESS_LEVEL_USER):
                print(f"Пользователь {temp_card} успешно добавлен.")
                access_granted(temp_card, temp_card, ACCESS_LEVEL_USER)
            else:
                print(f"Ошибка при добавлении пользователя: карта ID {temp_card} уже существует.")
                indicate_access_denied()
        else:
            name, temp_access_level = user
            if temp_access_level == ACCESS_LEVEL_SUPER_ADMIN:
                print(f"Выключение режима. Приложена карта уровня {temp_access_level}.")
                indicate_access_granted()
                break
            else:
                print(f"Пользователь уже добавлен в БД: {name} (ID карты: {temp_card} Уровень доступа: {temp_access_level}.)")
                access_granted(name, temp_card, temp_access_level)

def access_granted(card_id, access_level):
    print(f"Доступ предоставлен:(ID карты: {card_id} access_level: {access_level}).")
    open_door(get_setting("door_open_time", 3))
    indicate_access_granted()

def access_denied(card_id, access_level):
    print (print(f"Доступ запрещён:(ID карты: {card_id} access_level: {access_level})."))
    indicate_access_denied()

def check_time_interval():
    print("Проверка временного интервала...\nУдерживайте карту у считывателя около 3 секунд.\nАвтоматический выход через 7 секунд.")
    list_card = []
    current_time = time.time()
    
    while True:
        if len(set(list_card)) > 1:
            print("Множество карт не равно 1. Приложена другая карта.")
            return False
        if len(list_card) > 2:
            return True
        if time.time() - current_time > 8:
            print("Превышено время ожидания.")
            return False
        
        card_id = get_card_id_RFID()
        time.sleep(0.5)
        list_card.append(card_id)
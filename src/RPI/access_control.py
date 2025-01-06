
import time
from DB.database_manager import add_user, check_access, delete_user, get_setting
from RPI.access_manager import *
from rfid_reader import get_card_id_RFID, read_card

def process_access(card_id, attach_card):
    print(f"Проверка ID карты в БД: {card_id},")
    user = check_access(card_id)
    if user:
        name, access_level = user
        match attach_card:
            case 0:
                access_granted(name, card_id, access_level)
            case 1:
                if access_level == 2 or access_level == 3:
                    print("Переход в режим добавления пользователей.")
                    if check_time_interval() == True:
                        print("Начало добавления пользователй. Для выхода приложите карту уровня 2 и выше.")
                        time.sleep(1.5)
                        while True:
                            card_id = get_card_id_RFID()
                            time.sleep(1.5)
                            user = check_access(card_id)
                            if user:
                                name, access_level = user
                                if access_level > 1:
                                    print("Добавление пользователей завершено. Пользователи добавлены.")
                                    indicate_access_granted()
                                    break
                                else:
                                    print(f"Пользователь с ID карты {card_id} уже существует. Он имеет уровень доступа {access_level}. Добавление отменено.")
                                    indicate_access_denied()
                            else:
                                add_user(card_id, card_id, 1)
                                print(f"Пользователь {card_id} успешно добавлен.")
                    else:
                        print("Добавление пользователей отменено. Приложена другая карта.")
                        indicate_access_denied()
                else:
                    access_granted(name, card_id, access_level)
            case 2:
                if access_level == 3:
                    print("Переход в режим удаления пользователей.")
                    print("Для начала удаления пользователей поднесите карту к считывателю.")
                    temp_card = get_card_id_RFID()
                    time.sleep(1.5)
                    if temp_card == card_id:
                        print("Начало удаления пользователей. Для выхода приложите карту уровня 3.")
                        while True:
                            temp_card = get_card_id_RFID()
                            time.sleep(1.5)
                            user = check_access(temp_card)
                            if user:
                                name, access_level = user
                                if access_level == 3:
                                    print("Удаление пользователей завершено. Пользователи удалены переход в штатный режим.")
                                    indicate_access_granted()
                                    break
                                else:
                                    delete_user(temp_card)
                                    print(f"Пользователь {temp_card} успешно удалён.")
                                    indicate_access_granted()
                                    continue
                            else:
                                print(f"Пользователь с ID карты {temp_card} не найден. Удаление отменено.")
                                indicate_access_denied()
                    else:
                        print("Удаление пользователей отменено. Приложена другая карта.")
                        indicate_access_denied()
                else:
                    access_granted(name, card_id, access_level)
            case 3:
                if access_level == 3:
                    print("Переход в режим открытого доступа и добаления пользователей.")
                    print("Для включения режима поднесите карту к считывателю.")
                    temp_card = get_card_id_RFID()
                    time.sleep(1.5)
                    if temp_card == card_id:
                        print("Включение режима. Для выхода приложите любую карту уровня 3.")
                        while True:
                            temp_card = get_card_id_RFID()
                            time.sleep(1.5)
                            user = check_access(temp_card)
                            if user is None:
                                if add_user(temp_card, temp_card, access_level=1):
                                    print(f"Пользователь {temp_card} успешно добавлен.")
                                    open_door(get_setting("door_open_time", 3))
                                    indicate_access_granted()
                                    break
                                else:
                                    print(f"Ошибка при добавлении пользователя: карта ID {temp_card} уже существует.")
                                    indicate_access_denied()
                                    break
                            else:
                                name, access_level = user
                                if access_level == 3:
                                    print(f"Выключение режима. Приложена карта уровня {access_level}.")
                                    indicate_access_granted()
                                    break
                                else:
                                    print(f"Пользователь уже добавлен в бд: {name} (ID карты: {temp_card}) access_level: {access_level}.")
                                    indicate_access_denied()
                                    break
                else:
                    access_granted(name, temp_card, access_level)

            case _:
                print("Доступ запрещён. Пользователь не найден. Карта не распознана. Приложите другую карту. Не правильно считана карта.")
                indicate_access_denied()

    else:
        print("Доступ запрещён. Пользователь не найден.")
        indicate_access_denied()




def access_granted(name, card_id, access_level):
    print(f"Доступ предоставлен: {name} (ID карты: {card_id}) access_level: {access_level}.")
    open_door(get_setting("door_open_time", 3))
    indicate_access_granted()

def access_denied(name, card_id, access_level):
    print(f"Доступ запрещён: {name} (ID карты: {card_id}) access_level: {access_level}.")
    indicate_access_denied()


def check_time_interval():
    print("Проверка временного интервала...\n Удерживайте карту к считывателю. около 3 секунд. Автоматически выход через 7 секунд.")
    list_card = []
    current_time = time.time()
    while True:
        card_id = get_card_id_RFID()
        time.sleep(1)
        list_card.append(card_id)
        if len(set(list_card)) > 1:
            print("Множество карт не равно 1. Приложена другая карта.")
            return False
        if len(list_card) > 2:
            return True
        else:
            if time.time() - current_time > 8:
                print("Превышено время ожидания.")
                return False
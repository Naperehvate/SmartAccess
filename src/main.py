import time
from rfid_reader import read_card
from database_manager import create_database, check_access

def main():
    create_database()  # Убедимся, что база данных создана
    while True:
        time.sleep(5)
        card_id, _ = read_card()
        if card_id:
            print(f"Считан ID карты: {card_id}")
            user = check_access(card_id)
            if user:
                print(f"Добро пожаловать, {user[0]}!")
            else:
                print("Доступ запрещён. Пользователь не найден.")
        else:
            print("Не удалось считать карту.")
        if(input("Продолжить? (y/n) ") != "y"): break

if __name__ == "__main__":
    main()

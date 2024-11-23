import sys
from rfid_reader import read_card
from database_manager import create_database, check_access
from admin_menu import admin_menu

def main():
    create_database()
    if sys.platform == "win32":
        admin_menu()
    else:
        while True:
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

if __name__ == "__main__":
    main()

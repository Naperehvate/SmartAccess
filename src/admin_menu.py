from database_manager import add_user, delete_user, check_access, log_event

def admin_menu():
    while True:
        print("\n--- Админ-меню ---")
        print("1. Добавить пользователя")
        print("2. Удалить пользователя")
        print("3. Эмуляция работы")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            card_id = input("Введите ID карты: ")
            name = input("Введите имя пользователя: ")
            access_level = input("Введите уровень доступа (1 - стандартный, 2 - админ): ")
            if not check_access(card_id):
                add_user(card_id, name, int(access_level))
            else:
                print(f"Пользователь с ID карты {card_id} уже существует. Добавление отменено.")

        elif choice == "2":
            card_id = input("Введите ID карты для удаления: ")
            delete_user(card_id)

        elif choice == "3":
            emulate_system()

        elif choice == "4":
            print("Выход из админ-меню.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

def emulate_system():
    print("\n--- Эмуляция работы системы ---")
    # Пример заранее зарегистрированных ID карт
    registered_cards = ["123456789", "987654321"]
    
    for card_id in ["123456789", "987654321", "555555555"]:  # Тестируем существующую и неизвестную карты
        log_event(f"Эмуляция проверки карты ID {card_id}.")
        print(f"\nПроверка карты ID {card_id}...")
        user = check_access(card_id)
        
        if user:
            print(f"Доступ предоставлен: {user[0]} (ID карты: {card_id}).")
        else:
            if card_id not in registered_cards:
                print(f"Карта ID {card_id} не зарегистрирована в системе.")
            else:
                print(f"Доступ запрещён для карты ID {card_id}: причина неизвестна.")

        

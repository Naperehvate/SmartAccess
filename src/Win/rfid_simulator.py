class SimpleMFRC522:
    @staticmethod
    def read():
        card_id = input("Введите ID карты (симуляция): ")
        return card_id, "TestCard"

    @staticmethod
    def write(data):
        print(f"Симуляция записи данных: {data}")

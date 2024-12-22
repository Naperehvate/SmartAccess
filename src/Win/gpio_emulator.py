class GPIO:
    @staticmethod
    def cleanup():
        print("Очистка GPIO (симуляция).")

    @staticmethod
    def setmode(mode):
        print(f"Установлен режим GPIO: {mode} (симуляция).")

    @staticmethod
    def setup(pin, mode):
        print(f"Настройка GPIO пина {pin} как {mode} (симуляция).")

    @staticmethod
    def output(pin, value):
        print(f"Запись значения {value} в GPIO пин {pin} (симуляция).")

import sys

if sys.platform == "win32":
    print("Запуск на Windows — эмуляция GPIO.")

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
        def input(pin):
            print(f"Чтение с GPIO пина {pin} (симуляция).")
            return 0

        @staticmethod
        def output(pin, value):
            print(f"Запись значения {value} в GPIO пин {pin} (симуляция).")

else:
    print("Запуск на Raspberry Pi — использование реальных GPIO.")
    import RPi.GPIO as GPIO

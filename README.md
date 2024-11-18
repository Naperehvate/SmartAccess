#
SmartAccess/
main.py                  # Главный файл для запуска программы
gpio_manager.py          # Управление GPIO (реальное или эмуляция)
rfid_reader.py           # Работа с RFID
database_manager.py      # Работа с базой данных
windows_simulation.py    # Эмуляция на Windows
rpi_simulation.py        # Работа на Raspberry Pi

Если запускаете на Windows, используйте команду: python main.py
Если запускаете на Raspberry Pi, убедитесь, что все зависимости установлены: pip install RPi.GPIO mfrc522
--> python main.py
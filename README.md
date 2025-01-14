# **Разработчики:**  
**Трофимов Е.**  
**Полушкин Н.**
# 📝 SmartAccess

**SmartAccess** — это система управления доступом с использованием RFID. Проект создан для удобного управления и эмуляции работы с оборудованием чтения RFID.

## 📂 Структура проекта

- **`src`**
  - **`DB`**
    - **`database_manager.py`**  
      Модуль для работы с базой данных.
  - **`RPI`**
    - **`access_control.py`**  
      Логика управления доступом.
    - **`access_manager.py`**  
      Управление правами доступа.
    - **`buzzer_controller.py`**  
      Управление зуммером.
    - **`led_controller.py`**  
      Управление LED-индикаторами.
    - **`operational_mode.py`**  
      Настройка режимов работы системы.
    - **`relay_controller.py`**  
      Управление реле для открытия дверей.
  - **`Win`**
    - **`config.py`**  
      Конфигурационный файл для настроек.
    - **`gpio_manager.py`**  
      Модуль для работы с GPIO, с поддержкой эмуляции.
    - **`rfid_reader.py`**  
      Модуль для работы с RFID-ридером.
    - **`main.py`**  
      Главный файл для запуска программы.
  - **`web_app`**
    - **`scripts/admin_menu.js`**  
      Скрипты для управления веб-интерфейсом.
    - **`static/styles.css`**  
      Стили для веб-интерфейса.
    - **`static/admin_menu.html`**  
      Интерфейс админ-панели.
    - **`static/index.html`**  
      Главная страница интерфейса.
    - **`static/user_list.html`**  
      Интерфейс управления пользователями.


## 🚀 Запуск
**Убедитесь, что Python установлен.**
### На Windows (эмуляция работы):
Запустите файл `main.py`.  

### На Raspberry Pi:
1. Удостоверьтесь, что все зависимотси установлены.  
    ```bash
    pip install RPi.GPIO mfrc522
2. Подключите RFID-ридер к контактам Raspberry Pi:  
   ```bash
   SDA  -> Pin 24
   SCK  -> Pin 23
   MOSI -> Pin 19
   MISO -> Pin 21
   GND  -> Pin 6
   RST  -> Pin 22
   3.3v -> Pin 1
3. Настройте интерфейс SPI:
Введите в терминале:  
   ```bash
   sudo raspi-config
   ``` 
    Выберите «5 Интерфейсы», затем «P4 SPI» и активируйте.
    Перезагрузите Raspberry Pi
   ```bash
   sudo reboot
   ```
    Проверьте включение SPI:
    ```bash
    lsmod | grep spi
    ```
    Если spi_bcm2835 не отображается, откройте конфигурацию:
    ```bash
    sudo nano /boot/config.txt
    ```
    Убедитесь, что строка dtparam=spi=on активна (без #).

4. Обновите систему:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
5. Установите зависимости:
   ```bash
   sudo apt install python3-dev python3-pip python3-venv
   python3 -m pip install spidev mfrc522
   ```
6. Запустите программу:
   ```bash
   python main.py
   ```

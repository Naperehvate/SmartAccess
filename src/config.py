
import sys
from DB.database_manager import create_database, set_setting
from RPI.operational_mode import run_operational_mode
from Win.admin_menu import admin_menu

def initialize_system():
    create_database()
    set_setting("door_open_time", 3)  # Устанавливаем время открытия двери по умолчанию
    if sys.platform == "win32":
        admin_menu()
    #else:
        run_operational_mode()

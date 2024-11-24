import os
import sqlite3

DB_NAME = "rfidDB.sqlite"

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

# Соединение с базой данных
    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"Соединение с базой данных {self.db_name} установлено.")

# Закрытие соединения с базой данных
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print(f"Соединение с базой данных {self.db_name} закрыто.")

# Выполнение запроса
    def execute(self, query, params=(), commit=False, fetchone=False, fetchall=False):
        if not self.conn:
            raise RuntimeError("База данных не подключена.")
        self.cursor.execute(query, params)
        if commit:
            self.conn.commit()
        if fetchone:
            return self.cursor.fetchone()
        if fetchall:
            return self.cursor.fetchall()

# Инициализация базы данных
    def initialize(self):
        self.connect()
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            access_level INTEGER DEFAULT 1
        )""", commit=True)
        self.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""", commit=True)
        print("Структура базы данных проверена и инициализирована.")

db_manager = DatabaseManager(DB_NAME)

# Инициализация базы данных 
def create_database():
    if not os.path.exists(DB_NAME):
        print(f"Создание базы данных {DB_NAME}...")
    db_manager.initialize()

# Записывает событие в лог
def log_event(event):
    db_manager.execute("INSERT INTO logs (event) VALUES (?)", (event,), commit=True)

# Добавляет пользователя в базу данных
def add_user(card_id, name, access_level=1):
    try:
        db_manager.execute(
            "INSERT INTO users (card_id, name, access_level) VALUES (?, ?, ?)",
            (card_id, name, access_level),
            commit=True
        )
        print(f"Пользователь {name} успешно добавлен.")
        log_event(f"Добавлен пользователь: {name}, карта ID: {card_id}, уровень доступа: {access_level}")
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким ID карты уже существует.")
        log_event(f"Ошибка при добавлении пользователя: карта ID {card_id} уже существует.")

# Удаляет пользователя из базы данных
def delete_user(card_id):
    """Удаляет пользователя из базы данных."""
    result = db_manager.execute(
        "DELETE FROM users WHERE card_id = ?", (card_id,), commit=True
    )
    if db_manager.cursor.rowcount > 0:
        print(f"Пользователь с ID карты {card_id} успешно удалён.")
        log_event(f"Удалён пользователь с картой ID: {card_id}")
    else:
        print("Пользователь с таким ID карты не найден.")
        log_event(f"Попытка удаления несуществующего пользователя с картой ID: {card_id}")

# Получает информацию о пользователе по ID карты
def get_user(card_id):
    return db_manager.execute(
        "SELECT name, access_level FROM users WHERE card_id = ?", (card_id,), fetchone=True
    )

# Проверяет доступ пользователя по ID карты
def check_access(card_id):
    user = get_user(card_id)
    if user:
        name, access_level = user
        if access_level < 1:
            log_event(f"Доступ запрещён: недостаточный уровень доступа для {name} (ID карты: {card_id}).")
            return None
        log_event(f"Доступ разрешён: {name} (ID карты: {card_id}).")
        return user
    else:
        log_event(f"Доступ запрещён: карта ID {card_id} отсутствует в базе данных.")
        return None

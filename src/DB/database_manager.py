import os
import sqlite3

DB_NAME = "rfidDB.sqlite"


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"Соединение с базой данных {self.db_name} установлено.")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print(f"Соединение с базой данных {self.db_name} закрыто.")

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

    def initialize(self):
        self.connect()
        self.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            access_level INTEGER DEFAULT 1
        )""", commit=True)

        self.execute("""CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""", commit=True)

        self.execute("""CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )""", commit=True)

        print("Структура базы данных проверена и инициализирована.")


# Создаем экземпляр DatabaseManager
db_manager = DatabaseManager(DB_NAME)


# Инициализация базы данных
def create_database():
    if not os.path.exists(DB_NAME):
        print(f"Создание базы данных {DB_NAME}...")
    db_manager.initialize()


# Логирование событий
def log_event(event_type, event_details=None):
    db_manager.execute(
        "INSERT INTO logs (event_type, event_details) VALUES (?, ?)",
        (event_type, event_details),
        commit=True
    )


# Работа с пользователями
def add_user(card_id, name, access_level=1):
    try:
        db_manager.execute(
            "INSERT INTO users (card_id, name, access_level) VALUES (?, ?, ?)",
            (card_id, name, access_level),
            commit=True
        )
        print(f"Пользователь {name} успешно добавлен.")
        log_event("USER_ADDED", f"Пользователь: {name}, карта ID: {card_id}, уровень доступа: {access_level}")
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким ID карты уже существует.")
        log_event("ERROR", f"Ошибка при добавлении пользователя: карта ID {card_id} уже существует.")


def delete_user(card_id):
    result = db_manager.execute(
        "DELETE FROM users WHERE card_id = ?", (card_id,), commit=True
    )
    if db_manager.cursor.rowcount > 0:
        print(f"Пользователь с ID карты {card_id} успешно удалён.")
        log_event("USER_DELETED", f"Удалён пользователь с картой ID: {card_id}")
    else:
        print("Пользователь с таким ID карты не найден.")
        log_event("ERROR", f"Попытка удаления несуществующего пользователя с картой ID: {card_id}")


def get_user(card_id):
    return db_manager.execute(
        "SELECT name, access_level FROM users WHERE card_id = ?", (card_id,), fetchone=True
    )


def check_access(card_id):
    user = get_user(card_id)
    if user:
        name, access_level = user
        if access_level < 1:
            log_event("ACCESS_DENIED", f"Недостаточный уровень доступа для {name} (ID карты: {card_id})")
            return None
        log_event("ACCESS_GRANTED", f"Доступ разрешён для {name} (ID карты: {card_id})")
        return user
    else:
        log_event("ACCESS_DENIED", f"Карта ID {card_id} отсутствует в базе данных")
        return None


# Работа с настройками
def set_setting(key, value):
    db_manager.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (key, value),
        commit=True
    )


def get_setting(key, default=None):
    result = db_manager.execute(
        "SELECT value FROM settings WHERE key = ?", (key,), fetchone=True
    )
    return result[0] if result else default

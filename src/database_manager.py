import os
import sqlite3

DB_NAME = "rfidDB.sqlite"

def create_database():
    if not os.path.exists(DB_NAME):
        print(f"Создание базы данных {DB_NAME}...")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Создание таблицы пользователей (если не существует)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        access_level INTEGER DEFAULT 1
        )
        """)

        # Создание таблицы логов (если не существует)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()
        print("База данных успешно создана.")
    else:
        print(f"База данных {DB_NAME} уже существует.")

def log_event(event):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (event) VALUES (?)", (event,))
    conn.commit()
    conn.close()

def add_user(card_id, name, access_level=1):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (card_id, name, access_level) VALUES (?, ?, ?)",
            (card_id, name, access_level)
        )
        conn.commit()
        conn.close()
        print(f"Пользователь {name} успешно добавлен.")
        log_event(f"Добавлен пользователь: {name}, карта ID: {card_id}, уровень доступа: {access_level}")
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким ID карты уже существует.")
        log_event(f"Ошибка при добавлении пользователя: карта ID {card_id} уже существует.")

def delete_user(card_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE card_id = ?", (card_id,))
    if cursor.rowcount > 0:
        print(f"Пользователь с ID карты {card_id} успешно удалён.")
        log_event(f"Удалён пользователь с картой ID: {card_id}")
    else:
        print("Пользователь с таким ID карты не найден.")
        log_event(f"Попытка удаления несуществующего пользователя с картой ID: {card_id}")
    conn.commit()
    conn.close()

def check_access(card_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, access_level FROM users WHERE card_id = ?", (str(card_id),))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        name, access_level = user
        if access_level < 1:
            log_event(f"Доступ запрещён: недостаточный уровень доступа для {name} (ID карты: {card_id}).")
            return None
        else:
            log_event(f"Доступ разрешен: {name} (ID карты: {card_id}).")
            return user
    else:
        log_event(f"Доступ запрещён: карта ID {card_id} отсутствует в базе данных.")
        return None

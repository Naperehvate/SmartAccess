import os
import sqlite3

DB_NAME = "rfidDB.sqlite"

def create_database():
    if not os.path.exists(DB_NAME):
        print(f"База данных {DB_NAME} не найдена. Создаём новую базу данных...")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            access_level INTEGER DEFAULT 1
        )
        """)

        conn.commit()
        conn.close()
        print("База данных и таблица 'users' успешно созданы.")
    else:
        print(f"База данных {DB_NAME} уже существует.")

def check_access(card_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE card_id = ?", (str(card_id),))
    user = cursor.fetchone()
    conn.close()
    return user

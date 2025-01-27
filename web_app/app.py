import sys
import os

from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.DB.database_manager import *

app = Flask(__name__)

# Инициализация базы данных перед использованием
create_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')

@app.route('/user_list')
def user_list():
    return render_template('user_list.html')

@app.route('/get_users')
def get_users():
    try:
        users = get_all_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Ошибка загрузки пользователей: {str(e)}"}), 500

@app.route('/add_user', methods=['POST'])
def add_user_route():
    try:
        data = request.get_json()
        card_id = data['card_id']
        name = data['name']
        access_level = int(data['access_level'])

        add_user(card_id, name, access_level)  # Добавляем пользователя в базу данных
        return jsonify({"message": "Пользователь успешно добавлен!"})
    except Exception as e:
        return jsonify({"error": f"Ошибка добавления пользователя: {str(e)}"}), 500

@app.route('/delete_user', methods=['POST'])
def delete_user_route():
    try:
        data = request.get_json()
        card_id = data['card_id']

        delete_user(card_id)  # Удаляем пользователя из базы данных
        return jsonify({"message": "Пользователь успешно удален!"})
    except Exception as e:
        return jsonify({"error": f"Ошибка удаления пользователя: {str(e)}"}), 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)

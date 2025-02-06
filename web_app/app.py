import sys
import os

from flask import Flask, render_template, request, jsonify # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.DB.database_manager import *

app = Flask(__name__)
create_database()

# Страницы
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')

@app.route('/user_list')
def user_list():
    return render_template('user_list.html')

@app.route('/access_history')
def access_history():
    return render_template('access_history.html')



# Работа с запросами
@app.route('/get_users')
def get_users():
    try:
        users = get_all_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Ошибка загрузки пользователей: {str(e)}"}), 500
    

@app.route('/accsess_history_logs')
def get_access_history():
    try:
        history = get_all_logs()
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": f"Ошибка загрузки истории доступа: {str(e)}"}), 500

@app.route('/add_user', methods=['POST'])
def add_user_route():
    try:
        data = request.get_json()
        card_id = data['card_id']
        name = data['name']
        access_level = int(data['access_level'])
        add_user(card_id, name, access_level)
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

@app.route('/edit_user', methods=['POST'])
def edit_user_route():
    try:
        data = request.get_json()
        card_id = data['card_id']
        new_name = data['new_name']
        
        if not user_exists(card_id):
            return jsonify({"error": "Пользователь с таким ID карты не найден"}), 404
            
        update_user_name(card_id, new_name)
        return jsonify({"message": "Имя пользователя успешно обновлено!"})
    except Exception as e:
        return jsonify({"error": f"Ошибка редактирования пользователя: {str(e)}"}), 500


# Авторизация

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        # Здесь должна быть логика проверки пользователя в базе данных     
        # Временная заглушка
        if username == "admin" and password == "admin":
            return jsonify({"message": "Авторизация успешна!"})
        else:
            return jsonify({"error": "Неверное имя пользователя или пароль"}), 401
    except Exception as e:
        return jsonify({"error": f"Ошибка авторизации: {str(e)}"}), 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)

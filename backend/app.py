# backend/app.py

from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

# Функция для подключения к базе данных PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host='database',
        port='5432',
        user='postgres',
        password='postgres',
        database='flask_app'
    )

# Функция для создания таблицы names, если она не существует
def create_names_table():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS names (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        ''')
        connection.commit()
    except psycopg2.Error as e:
        print(f'Error creating names table: {e}')
    finally:
        if connection:
            cursor.close()
            connection.close()

# Создаем таблицу names при запуске приложения
create_names_table()

# Маршрут для отображения HTML-формы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для сохранения имени в базе данных
@app.route('/save_name', methods=['POST'])
def save_name():
    name = request.form['name']
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO names (name) VALUES (%s)', (name,))
        connection.commit()
        return 'Name saved successfully!'
    except psycopg2.Error as e:
        return f'Error saving name: {e}'
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

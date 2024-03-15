from flask import Flask, request, render_template
import psycopg2
import redis

app = Flask(__name__, template_folder='../templates')

# Подключение к Redis
redis_host = 'redis'
redis_port = 6379
redis_db = 0
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# Функция для подключения к базе данных PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host='database',
        port='5432',
        user='postgres',
        password='postgres',
        database='flask_app'
    )

# Функция для создания таблицы users, если она не существует
def create_users_table():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                surname VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                login VARCHAR(100) NOT NULL
            )
        ''')
        connection.commit()
    except psycopg2.Error as e:
        print(f'Error creating users table: {e}')
    finally:
        if connection:
            cursor.close()
            connection.close()

# Создаем таблицу users при запуске приложения
create_users_table()

# Маршрут для отображения HTML-формы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для сохранения данных в базе данных
@app.route('/save_data', methods=['POST'])
def save_data():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    login = request.form['login']

    # Проверка на уникальность логина
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('SELECT login FROM users WHERE login = %s', (login,))
        existing_login = cursor.fetchone()
        if existing_login:
            return '<script>alert("Login already exists!"); window.location.replace("/")</script>'
    except psycopg2.Error as e:
        return f'Error checking login: {e}'
    finally:
        if connection:
            cursor.close()
            connection.close()

    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, surname, email, login) VALUES (%s, %s, %s, %s)',
                       (name, surname, email, login))
        connection.commit()

        # Кэширование данных в Redis
        redis_conn.set(login, f'{name} {surname}')

        return '<script>alert("Data saved successfully!"); window.location.replace("/")</script>'
    except psycopg2.Error as e:
        return f'Error saving data: {e}'
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

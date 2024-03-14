# Используем базовый образ Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей внутрь контейнера и устанавливаем их
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Копируем все файлы из текущего каталога внутрь контейнера
COPY . .

# Устанавливаем переменные окружения для настройки PostgreSQL
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB database

# Команда, которая будет запущена при старте контейнера
CMD ["python", "backend/app.py"]

# Используем официальный образ Python
FROM python:3.10

# Установка системных зависимостей, если они нужны
# RUN apt-get update && apt-get install -y --no-install-recommends <package>

# Установка sqlalchemy
RUN pip install sqlalchemy psycopg2-binary

# Копирование скрипта внутрь контейнера
COPY script.py /app/

# Установка рабочего каталога
WORKDIR /app

# Запуск скрипта при старте контейнера
CMD ["python", "./script.py"]
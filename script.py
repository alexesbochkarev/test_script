from sqlalchemy import create_engine, text

# db credentials
DB_USERNAME = "myuser"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "127.0.0.1"
DB_PORT =  "5432"
DB_NAME = "postgres"

connection_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создание соединения с базой данных
engine = create_engine(connection_url)

# Проверка соединения
try:
    with engine.connect() as connection:
        # Проверка соединения
        version = connection.execute(text("SELECT version()")).scalar()
        print(f"Версия PostgreSQL: {version}")
except Exception as e:
    print("Ошибка при подключении к базе данных:", e)


# SQL-запросы для создания таблиц и вставки тестовых данных
create_tables_query = """
    CREATE TABLE IF NOT EXISTS short_names (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        status BOOLEAN NOT NULL
    );

    CREATE TABLE IF NOT EXISTS full_names (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        status BOOLEAN NOT NULL
    );
"""

insert_data_query = """
    INSERT INTO short_names (name, status) VALUES
    ('file1', '1'),
    ('file2', '1'),
    ('file3', '1'),
    ('file4', '1'),
    ('file5', '1'),
    ('file6', '1')
    ON CONFLICT DO NOTHING;

    INSERT INTO full_names (name, status) VALUES
    ('file1.wav', '0'),
    ('file2.wav', '0'),
    ('file3.mp3', '0'),
    ('file4.mp3', '0'),
    ('file5.wav', '0'),
    ('file6.jpg', '0')
    ON CONFLICT DO NOTHING;
"""

# SQL-запрос для обновления данных в таблице full_names
update_query = """
    UPDATE full_names
    SET status = short_names.status
    FROM short_names
    WHERE full_names.name LIKE short_names.name || '.' || '%'
    AND NOT EXISTS (
        SELECT 1
        FROM short_names AS s
        WHERE s.name || '.' || REGEXP_REPLACE(full_names.name, short_names.name || '.' || '([^.]+)$', '') = full_names.name
        AND s.status <> short_names.status
    );
"""

# Выполнение запросов
with engine.connect() as connection:
    connection.execute(text(create_tables_query))
    connection.execute(text(insert_data_query))
    connection.execute(text(update_query))
    connection.commit()

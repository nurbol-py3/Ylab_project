Написать проект на FastAPI с использованием PostgreSQL в качестве БД. 
В проекте следует реализовать REST API по работе с меню ресторана, 
все CRUD операции. Для проверки задания, к презентаций будет приложена 
Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.


1. Установка зависимостей:

pip install fastapi[all] sqlalchemy psycopg2


2. Настройка подключения к базе данных(database.py):

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

Замените user, password, localhost, dbname на свои реальные данные.

3. Запуск приложения:

   uvicorn main:app --reload

4. Если ошибки с базы данных очистить с помощью команды:

server = postgres = кнопка "запросник" = TRUNCATE TABLE menus CASCADE;

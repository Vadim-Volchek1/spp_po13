📌 Employment Center API
FastAPI + SQLAlchemy + PostgreSQL

📖 Описание проекта
Проект представляет собой REST API для работы с базой данных центра занятости населения.
Реализованы сущности:

Соискатели (Citizens)

Работодатели (Employers)

Вакансии (Vacancies)

Отклики (Applications)

Навыки (Skills)

API позволяет выполнять полный набор CRUD‑операций:
создание, чтение, обновление и удаление записей.

🏗 Используемые технологии
Python 3.10+

FastAPI — веб‑фреймворк

SQLAlchemy — ORM для работы с PostgreSQL

PostgreSQL — база данных

Uvicorn — ASGI‑сервер

Pydantic — валидация данных

📁 Структура проекта
src/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── config.py
│   └── routers/
│       ├── citizens.py
│       ├── employers.py
│       ├── vacancies.py
│       ├── applications.py
│       └── skills.py
│
├── venv/
├── requirements.txt
└── .env

⚙️ Настройка окружения
1. Создать виртуальное окружение
   python -m venv venv

2. Активировать окружение
   venv\Scripts\activate

3. Установить зависимости
   pip install -r requirements.txt

🗄 Настройка подключения к базе данных
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/Center_data

🚀 Запуск проекта
uvicorn app.main:app --reload

После запуска сервер будет доступен по адресу:

👉 http://127.0.0.1:8000

Документация Swagger UI:

👉 http://127.0.0.1:8000/docs

📚 Реализованные эндпойнты
Каждая сущность имеет набор маршрутов:

GET /<entity> — получить список

GET /<entity>/{id} — получить по ID

POST /<entity> — создать запись

PUT /<entity>/{id} — обновить запись

DELETE /<entity>/{id} — удалить запись

Например:

/citizens

/employers

/vacancies

/applications

/skills


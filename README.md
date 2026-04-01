# UGC Polls - Test Task for 'Absolut'

Django-api для опросов/анкетирования с поддержкой REST API.

## Features

- Бэкенд на Django 6.0+
- REST API на Django REST Framework
- Поддержка PostgreSQL (с fallback на SQLite для разработки)
- Контейнеризация с Docker
- Конфигурация через переменные окружения
- Автоматическое заполнение базы тестовыми данными
- Отслеживание сессий опроса
- Валидация при отправке ответов


## Начало работы

### Требования

- Python 3.13+
- Docker и Docker Compose

### Настройка окружения

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd ugc-polls
   ```

2. Создайте файл окружения:
   ```bash
   cp .env.example .env
   ```

3. Отредактируйте `.env`:
   - `DEBUG=True` для разработки
   - `SECRET_KEY` - сгенерируйте безопасный ключ
   - `DATABASE_URL` - для PostgreSQL

### Запуск через Docker

```bash
docker-compose up --build
```

Будет выполнено:
1. Сборка Docker-образа
2. Запуск контейнера
3. Применение миграций
4. Заполнение базы тестовыми данными
5. Запуск сервера разработки

Приложение будет доступно по адресу: http://localhost:8000

### Локальный запуск (без Docker)

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -e .
   ```

3. Примените миграции:
   ```bash
   python src/manage.py migrate
   ```

4. Заполните базу тестовыми данными:
   ```bash
   python src/manage.py seed_data
   ```

5. Запустите сервер:
   ```bash
   python src/manage.py runserver 0.0.0.0:8000
   ```

Приложение будет доступно по адресу: http://localhost:8000

### Качество кода

Проект использует Ruff для проверки качества кода:

```bash
ruff check .
```

Автоисправление:

```bash
ruff check . --fix
```

## Комментарии по оптимизации под нагрузку
- Индексы: все внешние ключи и часто фильтруемые поля покрыты индексами (db_index=True или indexes в Meta).

- select_related / prefetch_related: в NextQuestionView используются для минимизации количества запросов.

- N+1 проблема: сериализаторы используют read_only=True и подгружают связанные данные через prefetch_related.


### Что также можно учесть
- Использование Daphne или Uvicorn для обработки асинхронных запросов.
- Поддержка WebSocket для real-time уведомлений о новых опросах.
- Асинхронные view с async def для неблокирующих I/O операций.

---
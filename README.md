# YaCut — URL Shortener

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet.svg)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Сервис для создания коротких ссылок с возможностью загрузки файлов на Яндекс.Диск.

## ✨ Возможности

- 🔗 **Сокращение ссылок** — генерация коротких URL автоматически или с кастомным идентификатором
- 📁 **Загрузка файлов** — асинхронная загрузка файлов на Яндекс.Диск с генерацией коротких ссылок
- 🔌 **REST API** — полноценный API для интеграции
- 🎨 **Веб-интерфейс** — простой и удобный UI
- 📋 **Postman-коллекция** — готовые тесты для проверки API

## 🛠 Технологический стек

- **Backend**: Flask 3.0, SQLAlchemy 2.0, Flask-Migrate
- **Async**: aiohttp (для интеграции с Яндекс.Диск)
- **Database**: SQLite (по умолчанию), совместим с PostgreSQL
- **Frontend**: Bootstrap 4
- **Package Manager**: [uv](https://docs.astral.sh/uv/)

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/your-username/yacut.git
cd yacut
```

### 2. Установка зависимостей (UV)

```bash
# Установка uv (если ещё не установлен)
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установка зависимостей и создание venv
uv sync

# Для разработки (с dev-зависимостями)
uv sync --dev
```

<details>
<summary>📦 Альтернатива: установка через pip</summary>

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Для разработки
pip install -r requirements-dev.txt
```

</details>

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта (см. `.env.example`):

```env
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your-yandex-disk-oauth-token  # опционально
```

### 4. Инициализация базы данных

```bash
uv run flask db upgrade
```

### 5. Запуск

```bash
uv run flask run
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

## 📡 API

### Создание короткой ссылки

```http
POST /api/id/
Content-Type: application/json

{
    "url": "https://example.com/very/long/url",
    "custom_id": "mylink"  // опционально
}
```

**Ответ (201 Created):**
```json
{
    "url": "https://example.com/very/long/url",
    "short_link": "http://localhost/mylink"
}
```

### Получение оригинальной ссылки

```http
GET /api/id/{short_id}/
```

**Ответ (200 OK):**
```json
{
    "url": "https://example.com/very/long/url"
}
```

### Ошибки API

| Код | Описание |
|-----|----------|
| 400 | Некорректные данные запроса |
| 404 | Короткая ссылка не найдена |

Полная спецификация API: [openapi.yml](openapi.yml)

## 🧪 Тестирование

### Pytest

```bash
uv run pytest
```

### Postman

В директории [`postman_collection/`](postman_collection/) находится готовая коллекция для тестирования API в Postman:

1. Импортируйте `Yacut.postman_collection.json` в Postman
2. Запустите скрипт подготовки данных: `bash postman_collection/set_up_data.sh`
3. Запустите коллекцию в Postman

Подробная инструкция: [postman_collection/README.md](postman_collection/README.md)

## 📂 Структура проекта

```
yacut/
├── yacut/
│   ├── __init__.py      # Инициализация Flask-приложения
│   ├── api_views.py     # REST API endpoints
│   ├── constants.py     # Константы приложения
│   ├── error_handlers.py # Обработка ошибок
│   ├── forms.py         # WTForms формы
│   ├── models.py        # SQLAlchemy модели
│   ├── views.py         # Веб-интерфейс
│   ├── yandex_disk.py   # Интеграция с Яндекс.Диск
│   ├── static/          # CSS, JS, изображения
│   └── templates/       # HTML-шаблоны
├── migrations/          # Миграции Alembic
├── tests/               # Pytest тесты
├── postman_collection/  # Postman-коллекция и документация
├── settings.py          # Конфигурация
├── pyproject.toml       # UV/Python конфигурация
├── requirements.txt     # Зависимости (fallback для pip)
└── openapi.yml          # OpenAPI спецификация
```

## 🔧 Конфигурация Яндекс.Диск

Для использования функции загрузки файлов:

1. Создайте приложение на [Яндекс.OAuth](https://oauth.yandex.ru/)
2. Получите OAuth-токен с правами `cloud_api:disk.app_folder`
3. Добавьте токен в переменную окружения `DISK_TOKEN`

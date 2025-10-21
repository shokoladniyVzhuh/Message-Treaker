# 📱 Message Treaker

> Автоматизация действий на основе сообщений в Telegram чатах

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Telethon](https://img.shields.io/badge/Telethon-1.30+-lightblue.svg)](https://docs.telethon.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Возможности

- 📱 Мониторинг Telegram чатов (личные и групповые)
- 🔔 Автоматические действия по триггерам
- ⏰ Управление будильниками
- 📊 Логирование срабатываний
- 🖥️ Веб-интерфейс для управления

## Архитектура

- **Python Watcher** - демон для мониторинга Telegram
- **FastAPI Backend** - REST API для управления
- **Flutter UI** - десктопное приложение
- **SQLite** - хранение правил и логов

## 🚀 Быстрый запуск

### Вариант 1: Полный автоматический запуск (рекомендуется)
```bash
./start.sh
```
Этот скрипт автоматически:
- Активирует виртуальное окружение
- Проверяет зависимости
- Запускает API сервер
- Запускает Telegram watcher
- Открывает веб-интерфейс в браузере

### Вариант 2: Python лаунчер
```bash
python3 start_full.py
```

### Вариант 3: Только API + веб-интерфейс
```bash
python3 start_app.py
```

## 📋 Установка (первый раз)

1. **Клонируй репозиторий:**
   ```bash
   git clone https://github.com/your-username/Message-Treaker.git
   cd Message-Treaker
   ```

2. **Создай виртуальное окружение:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установи зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настрой Telegram API:**
   ```bash
   cp .env.example .env
   # Отредактируй .env и добавь свои API ключи с https://my.telegram.org/apps
   ```

## 🔧 Ручной запуск (для отладки)

1. **API сервер:**
   ```bash
   python3 run_api.py
   ```
2. **Watcher (в другом терминале):**
   ```bash
   python3 run_watcher.py
   ```
3. **Веб-интерфейс:**
   Открой `web/index.html` в браузере

## Первый запуск

При первом запуске watcher попросит авторизацию в Telegram:
- Введи номер телефона
- Введи код из SMS
- При необходимости введи 2FA пароль

## API Endpoints

- `GET /health` - статус сервиса
- `GET /rules` - список правил
- `POST /rules` - создать правило
- `GET /rules/{id}` - получить правило
- `PUT /rules/{id}` - обновить правило
- `DELETE /rules/{id}` - удалить правило
- `GET /hits` - история срабатываний

## Типы действий

- `alarm` - проиграть звук будильника
- `notify` - показать уведомление
- `command` - выполнить команду

## 🔒 Безопасность

⚠️ **Важно**: Это userbot - используй только со своим аккаунтом!
- Включи 2FA в Telegram
- Не злоупотребляй API
- Храни сессию в безопасном месте

## 🤝 Вклад в проект

1. Форкни репозиторий
2. Создай ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируй изменения (`git commit -m 'Add amazing feature'`)
4. Отправь в ветку (`git push origin feature/amazing-feature`)
5. Открой Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🐛 Сообщить об ошибке

Если вы нашли ошибку, создайте [Issue](https://github.com/your-username/Message-Treaker/issues) с подробным описанием.

## 📞 Поддержка

Если у вас есть вопросы, создайте [Discussion](https://github.com/your-username/Message-Treaker/discussions).

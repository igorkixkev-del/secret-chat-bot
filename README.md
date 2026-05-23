# Secret Chat Bot for Telegram

Защищённый чат-бот для Telegram с поддержкой сквозного шифрования и приватных переписок.

## Возможности

- 🔐 Сквозное шифрование сообщений (end-to-end encryption)
- 👤 Приватные одиночные чаты между пользователями
- 🔑 Управление ключами шифрования
- 📱 Простой и интуитивный интерфейс
- ⚡ Быстрые и надёжные сообщения
- 🛡️ Защита от несанкционированного доступа

## Требования

- Python 3.9+
- pip (менед��ер пакетов Python)
- Telegram Bot Token (получить на [@BotFather](https://t.me/botfather))

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/igorkixkev-del/secret-chat-bot.git
cd secret-chat-bot
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` с вашим токеном:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Использование

Запустите бота:
```bash
python bot.py
```

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/newchat @username` - Начать новый секретный чат с пользователем
- `/list` - Показать список активных чатов
- `/settings` - Параметры безопасности

## Архитектура

```
secret-chat-bot/
├── bot.py                 # Основной файл бота
├── config.py              # Конфигурация
├── crypto.py              # Модуль шифрования
├── database.py            # Работа с БД
├── handlers.py            # Обработчики команд
├── requirements.txt       # Зависимости
└── .env.example           # Пример .env файла
```

## Безопасность

- Все сообщения зашифрованы с использованием AES-256
- Ключи хранятся безопасно в локальной БД
- Поддержка двухфакторной аутентификации

## Лицензия

MIT License - см. файл LICENSE

## Автор

Создано igorkixkev-del

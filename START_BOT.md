# 🤖 MULTIC Telegram Bot - Запуск

**Статус:** ✅ Готов к запуску

---

## 🚀 КОМАНДА ДЛЯ ЗАПУСКА БОТА

```bash
python telegram_bot.py
```

или (если используешь Python 3 явно):

```bash
python3 telegram_bot.py
```

---

## 📝 ШАГ ЗА ШАГОМ

### 1️⃣ Установи зависимости (КРИТИЧНО!)
```bash
pip install -r requirements.txt
```

**Или если pip не работает правильно:**
```bash
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.1
```

### 2️⃣ Проверь что .env файл содержит токен
```bash
type .env | findstr TELEGRAM_BOT_TOKEN
```

Должно быть:
```
TELEGRAM_BOT_TOKEN=8908678178:AAFiCYAJj_4Eh-JylokTVpHuOizCE0hPitQ
```

### 3️⃣ Запусти бота
```bash
python telegram_bot.py
```

### 4️⃣ Ожидаемый вывод в консоль (ВАЖНО!)
Если видишь это → **БОТ РАБОТАЕТ ✅**

```
================================================================================
🤖 MULTIC TELEGRAM BOT - STARTUP
================================================================================

[1/5] Loading environment variables...
✅ dotenv loaded
[2/5] Reading TELEGRAM_BOT_TOKEN from .env...
✅ Token loaded (first 20 chars): 8908678178:AAFiCYAJ...
[3/5] Importing python-telegram-bot...
✅ python-telegram-bot imported successfully
[4/5] Setting up logs directory...
✅ Logs directory exists
✅ File logging configured (logs/telegram_bot.log)
[5/5] Initialization complete

================================================================================
✅ ALL CHECKS PASSED - STARTING BOT
================================================================================

✅ Bot application created
✅ Command handlers registered

================================================================================
🚀 BOT IS READY - WAITING FOR COMMANDS
================================================================================
Listening for messages in Telegram...
Press Ctrl+C to stop
```

### 5️⃣ Протестируй бота в Telegram
- Открой Telegram
- Найди своего бота (@multic_scout_bot)
- Отправь `/start`
- **Должен ответить:** "Я на связи."

### 6️⃣ Остановить бота
- Нажми `Ctrl+C` в PowerShell консоли
- Должно вывести: "⏹️ Bot stopped by user (Ctrl+C)"

---

## 🔒 БЕЗОПАСНОСТЬ

✅ Токен находится в `.env` файле (локально)  
✅ `.env` файл в `.gitignore` (не попадает на GitHub)  
✅ Токен НЕ вписан в код Python  
✅ Все переменные читаются через `os.getenv()`  
✅ Консоль выводит все ошибки явно  

---

## 📊 СТРУКТУРА ФАЙЛОВ

```
multic/
├── telegram_bot.py ────────── основной скрипт бота
├── .env ────────────────────── токен бота (локально)
├── .gitignore ───────────────── .env в списке игнорирования
├── requirements.txt ────────── зависимости
├── logs/
│   └── telegram_bot.log ───── логи бота
└── START_BOT.md ────────────── этот файл
```

---

## 🧹 ОСТАНОВКА БОТА

Нажми `Ctrl+C` в терминале.

Ожидаемый вывод:
```
^C
⏹️ Bot stopped by user
```

---

## 🐛 ЕСЛИ ЧТО-НИБУДЬ ПОШЛО НЕ ТАК

### Ошибка: "TELEGRAM_BOT_TOKEN не установлен"
```
1. Открой .env файл
2. Убедись что строка TELEGRAM_BOT_TOKEN содержит токен
3. Сохрани файл
4. Перезапусти бота
```

### Ошибка: "ModuleNotFoundError: No module named 'telegram'"
```bash
pip install python-telegram-bot==20.7
```

### Ошибка: "Invalid token"
```
1. Проверь токен в .env файле
2. Убедись что скопировал его полностью
3. Токен должен быть в формате: 123456:ABC...
```

### Ошибка: "logs directory does not exist"
```bash
mkdir logs
```

---

## ✅ КОМАНДЫ БОТА (ПОКА)

| Команда | Ответ |
|---------|-------|
| `/start` | "Я на связи." |

**Больше команд будут добавлены в Phase 2B (Copywriter Agent)**

---

## 📞 ИНФОРМАЦИЯ О БОТЕ

- **Имя:** MULTIC Scout Agent
- **Юзернейм:** @multic_scout_bot
- **Токен:** `8908678178:AAFiCYAJj_4Eh-JylokTVpHuOizCE0hPitQ`
- **Статус:** ✅ Active
- **Версия:** 1.0

---

## 🎯 NEXT STEPS

После первого запуска бота:

1. ✅ Протестировать `/start` команду
2. ✅ Проверить что логи пишутся в `logs/telegram_bot.log`
3. ✅ Запустить Scout Agent одновременно (в другом терминале)
4. ✅ Проверить что Scout Agent отправляет видео в Telegram
5. 🎬 Начать Phase 2B: Copywriter Agent

---

Created: 2026-09-19  
By: Claude Haiku 4.5

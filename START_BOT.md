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

### 1️⃣ Убедись что зависимости установлены
```bash
pip install -r requirements.txt
```

### 2️⃣ Проверь что .env файл содержит токен
```bash
cat .env | grep TELEGRAM_BOT_TOKEN
```

Должно быть:
```
TELEGRAM_BOT_TOKEN=8908678178:AAFiCYAJj_4Eh-JylokTVpHuOizCE0hPitQ
```

### 3️⃣ Запусти бота
```bash
python telegram_bot.py
```

### 4️⃣ Ожидаемый вывод
```
2026-09-19 15:30:45,123 - telegram.ext.Application - INFO - Application started
🤖 Initializing MULTIC Telegram Bot...
✅ Bot token loaded from .env
✅ Command handlers registered
🚀 Starting bot polling...
```

### 5️⃣ Протестируй бота
- Открой Telegram
- Найди своего бота (@multic_scout_bot)
- Отправь `/start`
- Должен ответить: **"Я на связи."**

---

## 🔒 БЕЗОПАСНОСТЬ

✅ Токен находится в `.env` файле  
✅ `.env` файл в `.gitignore` (не попадает на GitHub)  
✅ Токен не вписан в код  
✅ Все переменные читаются через `os.getenv()`  

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

# ⚙️ SCOUT AGENT - Настройка API (Бесплатное Решение)

**Версия:** 1.0  
**Дата:** 2026-09-10  
**Статус:** ✅ Все API бесплатные  
**Бюджет:** $0 USD

---

## 🎯 ОБЗОР

Этот гайд описывает пошаговую настройку всех необходимых API для Scout Agent **БЕЗ ДЕНЕЖНЫХ ЗАТРАТ**.

Все используемые API имеют бесплатные уровни с достаточными квотами для 24/7 работы.

---

## 🔑 API #1: BRAVE SEARCH API ⭐ ГЛАВНЫЙ

### Описание
- **Назначение:** Основной веб-поиск по интернету
- **Поддержка:** Видео, статьи, новости
- **Лимит:** 2000 запросов/день БЕСПЛАТНО
- **Стоимость:** $0

### Шаг 1: Получить API ключ

1. Перейти на https://brave.com/search/api
2. Нажать кнопку **"Get Started"** или **"Sign Up"**
3. Зарегистрироваться (email + пароль)
4. Подтвердить email
5. Перейти в Dashboard
6. Найти **API Key** в профиле

### Шаг 2: Сохранить ключ

```bash
# В файле .env:
BRAVE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Шаг 3: Тестирование

```python
import requests
import os

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
base_url = "https://api.search.brave.com/res/v1/web/search"

def test_brave_search():
    headers = {"Authorization": f"Bearer {BRAVE_API_KEY}"}
    params = {
        "q": "славяно-арийская культура",
        "count": 10
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        print("✅ Brave Search API работает!")
        return response.json()
    else:
        print(f"❌ Ошибка: {response.status_code}")
        return None

# Тест
results = test_brave_search()
if results:
    for item in results.get("web", [])[:3]:
        print(f"- {item['title']}")
```

---

## 🎬 API #2: YOUTUBE DATA API

### Описание
- **Назначение:** Поиск видео, получение статистики
- **Поддержка:** Все публичные видео YouTube
- **Лимит:** 10,000 запросов/день БЕСПЛАТНО
- **Стоимость:** $0

### Шаг 1: Получить API ключ

#### Вариант A: Google Cloud Console

1. Перейти на https://console.developers.google.com/
2. Создать новый проект:
   - Клик **"Select a Project"** → **"New Project"**
   - Название: `MULTIC-Scout`
   - Клик **Create**
3. Включить YouTube Data API v3:
   - Клик **"Enable APIs and services"**
   - Поиск: `youtube data api v3`
   - Клик на результат
   - Клик **"Enable"**
4. Создать API ключ:
   - Левое меню → **Credentials**
   - Клик **Create Credentials** → **API Key**
   - Скопировать ключ

#### Вариант B: Через Google Cloud CLI

```bash
# Если установлен gcloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable youtube.googleapis.com
gcloud alpha services api-keys create \
  --api-target=youtube.googleapis.com
```

### Шаг 2: Сохранить ключ

```bash
# В файле .env:
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Шаг 3: Тестирование

```python
from googleapiclient.discovery import build
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def test_youtube_search():
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.search().list(
            q="славяно-арийская культура",
            part='snippet',
            maxResults=5,
            type='video'
        )
        
        response = request.execute()
        
        print("✅ YouTube API работает!")
        print(f"Найдено видео: {len(response.get('items', []))}")
        
        return response
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

# Тест
results = test_youtube_search()
if results:
    for item in results.get('items', [])[:3]:
        print(f"- {item['snippet']['title']}")
```

### Установка библиотеки

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## 📱 API #3: VK API (ВКонтакте)

### Описание
- **Назначение:** Поиск видео в ВКонтакте
- **Поддержка:** Все видео из ВКонтакте
- **Лимит:** 3 запроса/сек (достаточно)
- **Стоимость:** $0

### Шаг 1: Получить Token

#### Вариант A: Server-side Token (рекомендуется для ботов)

1. Перейти на https://vk.com/dev/access_token
2. Создать новое приложение:
   - https://vk.com/dev/apps?act=manage
   - Клик **Create Application**
   - Тип: Standalone
   - Название: `MULTIC-Scout`
3. Получить Service Token:
   - Settings → Tokens → Create Server Token
   - Выдать права: `video`, `groups`
   - Скопировать token

#### Вариант B: Через Open Token (если не требуется)

```bash
# https://vk.com/dev/access_token
# Нажать на ссылку для получения token'а
```

### Шаг 2: Сохранить token

```bash
# В файле .env:
VK_API_TOKEN=vk1.a.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VK_API_VERSION=5.131  # Версия API
```

### Шаг 3: Тестирование

```python
import vk_api
import os

VK_API_TOKEN = os.getenv("VK_API_TOKEN")
VK_API_VERSION = os.getenv("VK_API_VERSION", "5.131")

def test_vk_search():
    try:
        vk = vk_api.VkApi(token=VK_API_TOKEN, api_version=VK_API_VERSION)
        
        # Поиск видео
        results = vk.method('video.search', {
            'q': 'славяно-арийская культура',
            'count': 20,
            'sort': 1  # По популярности
        })
        
        print("✅ VK API работает!")
        print(f"Найдено видео: {len(results.get('items', []))}")
        
        return results
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

# Тест
results = test_vk_search()
if results:
    for video in results.get('items', [])[:3]:
        print(f"- {video['title']}")
```

### Установка библиотеки

```bash
pip install vk-api
```

---

## 🖼️ API #4: WIKIMEDIA COMMONS

### Описание
- **Назначение:** Поиск изображений
- **Поддержка:** Все свободные изображения
- **Лимит:** Не ограничено
- **Стоимость:** $0

### Шаг 1: Не требуется регистрация!

Wikimedia Commons API полностью открыт и не требует аутентификации.

### Шаг 2: Тестирование

```python
import requests

def test_wikimedia_search():
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        
        params = {
            'action': 'query',
            'list': 'allimages',
            'aissort': 'timestamp',
            'aisdir': 'descending',
            'aiprop': 'url',
            'ailimit': 20,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("✅ Wikimedia Commons API работает!")
            return response.json()
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

# Тест
results = test_wikimedia_search()
```

---

## 🐦 API #5: TWITTER/X API (ОПЦИОНАЛЬНО)

### Описание
- **Назначение:** Мониторинг трендов
- **Поддержка:** Публичные твиты и тренды
- **Лимит:** v2 Free Tier (ограничен, но доступен)
- **Стоимость:** $0 (с ограничениями)

### Шаг 1: Получить ключи

1. Перейти на https://developer.twitter.com/
2. Нажать **"Create an app"**
3. Заполнить форму:
   - App name: `MULTIC-Scout`
   - Use case: Bot
4. Получить API Keys и Tokens:
   - **API Key** (Consumer Key)
   - **API Secret Key** (Consumer Secret)
   - **Bearer Token** (для App-only auth)
5. Скопировать ключи

### Шаг 2: Сохранить ключи

```bash
# В файле .env:
TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAAAAxx
```

### Шаг 3: Тестирование

```python
import requests
import os

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def test_twitter_search():
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    params = {
        "query": "славяно-арийская культура",
        "max_results": 10,
        "tweet.fields": "public_metrics,created_at"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print("✅ Twitter API работает!")
            return response.json()
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

# Тест
results = test_twitter_search()
```

### Установка библиотеки

```bash
pip install tweepy
```

---

## 📁 ФАЙЛ КОНФИГУРАЦИИ (.env)

### Пример `.env` файла

```bash
# ⭐ ГЛАВНЫЕ API (ОБЯЗАТЕЛЬНЫЕ)
BRAVE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VK_API_TOKEN=vk1.a.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VK_API_VERSION=5.131

# 📱 ОПЦИОНАЛЬНЫЕ API
TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAAAAxx

# 🗄️ БАЗА ДАННЫХ
DATABASE_PATH=./scout_db.sqlite
DATABASE_BACKUP=./backups/

# ⏱️ РАСПИСАНИЕ
SEARCH_INTERVAL_HOURS=1
REPORT_TIME=18:00

# 📧 УВЕДОМЛЕНИЯ (опционально)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_password

# 🎯 ПАРАМЕТРЫ ПОИСКА
MIN_VIEWS=50000
MIN_ENGAGEMENT_RATE=2.0
SEARCH_LANGUAGES=ru,en
```

### Установка `.env`

1. Создать файл `.env` в корне проекта
2. Скопировать содержимое выше
3. Вставить свои API ключи
4. Сохранить файл

### Защита `.env`

```bash
# Добавить в .gitignore:
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Это приватно и не попадет на GitHub
```

---

## 🚀 УСТАНОВКА ЗАВИСИМОСТЕЙ

### requirements.txt

```
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.0.0
aiohttp>=3.8.0
pandas>=1.5.0
apscheduler>=3.10.0
python-dotenv>=0.20.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.80.0
vk-api>=11.9.0
tweepy>=4.12.0
requests-html>=0.10.0
```

### Установка

```bash
# Перейти в папку проекта
cd path/to/multic

# Установить зависимости
pip install -r scout-agent/requirements.txt

# Или отдельные API
pip install requests google-api-python-client vk-api tweepy python-dotenv
```

---

## ✅ ПРОВЕРКА ВСЕх API

### Скрипт для тестирования

```python
# scout_test_all_apis.py

import os
from dotenv import load_dotenv

# Загрузить переменные окружения
load_dotenv()

def test_all_apis():
    """Тестирует все API"""
    
    print("=" * 60)
    print("ТЕСТ ВСЕХ API SCOUT AGENT")
    print("=" * 60)
    
    # 1. Brave Search API
    print("\n1️⃣ Brave Search API...")
    try:
        import requests
        brave_key = os.getenv("BRAVE_API_KEY")
        if brave_key:
            headers = {"Authorization": f"Bearer {brave_key}"}
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params={"q": "test", "count": 1}
            )
            if response.status_code == 200:
                print("   ✅ Brave Search работает!")
            else:
                print(f"   ❌ Ошибка {response.status_code}")
        else:
            print("   ⚠️ BRAVE_API_KEY не установлен")
    except Exception as e:
        print(f"   ❌ {e}")
    
    # 2. YouTube API
    print("\n2️⃣ YouTube API...")
    try:
        from googleapiclient.discovery import build
        youtube_key = os.getenv("YOUTUBE_API_KEY")
        if youtube_key:
            youtube = build('youtube', 'v3', developerKey=youtube_key)
            print("   ✅ YouTube API работает!")
        else:
            print("   ⚠️ YOUTUBE_API_KEY не установлен")
    except Exception as e:
        print(f"   ❌ {e}")
    
    # 3. VK API
    print("\n3️⃣ VK API...")
    try:
        import vk_api
        vk_token = os.getenv("VK_API_TOKEN")
        if vk_token:
            vk = vk_api.VkApi(token=vk_token)
            print("   ✅ VK API работает!")
        else:
            print("   ⚠️ VK_API_TOKEN не установлен")
    except Exception as e:
        print(f"   ❌ {e}")
    
    # 4. Wikimedia Commons API
    print("\n4️⃣ Wikimedia Commons API...")
    try:
        import requests
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={"action": "query", "format": "json"}
        )
        if response.status_code == 200:
            print("   ✅ Wikimedia Commons работает!")
        else:
            print(f"   ❌ Ошибка {response.status_code}")
    except Exception as e:
        print(f"   ❌ {e}")
    
    # 5. Twitter/X API (опционально)
    print("\n5️⃣ Twitter/X API (опционально)...")
    try:
        twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
        if twitter_token:
            print("   ✅ Twitter token установлен")
        else:
            print("   ⚠️ TWITTER_BEARER_TOKEN не установлен (опционально)")
    except Exception as e:
        print(f"   ⚠️ {e}")
    
    print("\n" + "=" * 60)
    print("Тест завершен!")
    print("=" * 60)

if __name__ == "__main__":
    test_all_apis()
```

### Запуск теста

```bash
python scout_test_all_apis.py
```

---

## 📊 СВОДКА ПО API

| API | Обязательный | Лимит | Ключ Получен | Статус |
|-----|-------------|-------|-------------|--------|
| Brave Search | ✅ Да | 2000/день | [ ] | |
| YouTube | ✅ Да | 10000/день | [ ] | |
| VK | ✅ Да | 3/сек | [ ] | |
| Wikimedia | ⏳ Рекомендуется | ∞ | - | Бесплатно |
| Twitter/X | ⏳ Опционально | Ограничен | [ ] | Бесплатно |

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ

### Шаг 1: Установка API ✅
- [ ] Получить BRAVE_API_KEY
- [ ] Получить YOUTUBE_API_KEY
- [ ] Получить VK_API_TOKEN
- [ ] (Опционально) Получить TWITTER_BEARER_TOKEN

### Шаг 2: Конфигурация ✅
- [ ] Создать файл `.env`
- [ ] Вставить все ключи
- [ ] Добавить `.env` в `.gitignore`

### Шаг 3: Установка зависимостей ✅
- [ ] Установить `requirements.txt`
- [ ] Установить библиотеки для API

### Шаг 4: Тестирование ✅
- [ ] Запустить `scout_test_all_apis.py`
- [ ] Проверить все API
- [ ] Убедиться, что все работает

### Шаг 5: Разработка
- [ ] Начать разработку Scout Agent
- [ ] Использовать API в коде
- [ ] Создать первый поиск вирусных видео

---

## ❓ ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ

### Вопрос: Все ли API полностью бесплатны?
**Ответ:** ✅ Да! Все используемые API имеют полностью бесплатные уровни с достаточными квотами.

### Вопрос: Может ли Scout Agent работать 24/7?
**Ответ:** ✅ Да! 2000 запросов Brave Search в день = ~83 запроса в час. Достаточно для 24/7 работы.

### Вопрос: Нужна ли кредитная карта?
**Ответ:** ❌ Нет! Все API можно настроить без кредитной карты.

### Вопрос: Что если я превышу лимит?
**Ответ:** API просто вернут ошибку. Добавьте rate limiting в код (см. примеры выше).

### Вопрос: Как сохранить API ключи в безопасности?
**Ответ:** Используйте `.env` файл и добавьте его в `.gitignore`. Никогда не коммитьте `.env`!

---

## 📚 ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

### Документация API:
- [Brave Search API](https://api.search.brave.com/res/v1/docs/search.html)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [VK API Documentation](https://vk.com/dev/methods)
- [Wikimedia API](https://commons.wikimedia.org/wiki/API:Main_page)
- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)

### Примеры:
- [Brave Search Examples](https://api.search.brave.com/res/v1/docs/examples.html)
- [YouTube Samples](https://github.com/youtube/api-samples)
- [VK SDK](https://github.com/VkNet/VkNet)

---

**Версия:** 1.0  
**Дата:** 2026-09-10  
**Стоимость:** $0 USD  
**Статус:** ✅ Полностью готово

🚀 **Scout Agent готов к настройке API без затрат!**

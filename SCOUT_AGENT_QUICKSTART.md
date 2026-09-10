# ⚡ SCOUT AGENT - БЫСТРЫЙ СТАРТ

**Время прочтения:** 5 минут  
**Время на подготовку:** 30 минут  
**Время на первый запуск:** 1 час  

---

## 🎯 ЧТО МЫ СДЕЛАЕМ

1. Получим бесплатные API ключи (15 мин)
2. Установим зависимости (10 мин)
3. Запустим тесты (5 мин)
4. Создадим первый скрипт (30 мин)

**Результат:** Рабочий Scout Agent, ищущий вирусные видео! ✅

---

## 📝 ШАГИ

### Шаг 1️⃣: Получить API Ключи (15 минут)

#### A. Brave Search API ⭐ (2 минуты)

```bash
# 1. Открыть браузер
https://brave.com/search/api

# 2. Нажать "Sign Up"
# 3. Создать аккаунт (email + пароль)
# 4. Подтвердить email
# 5. Скопировать API Key из профиля
```

**Ключ будет выглядеть так:**
```
BRAVE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

#### B. YouTube API (5 минут)

```bash
# 1. Открыть
https://console.developers.google.com/

# 2. Создать новый проект
# Название: MULTIC-Scout

# 3. Перейти в "Enable APIs and services"
# Поиск: youtube data api v3
# Нажать Enable

# 4. Перейти в Credentials
# Create Credentials → API Key
# Скопировать ключ
```

**Ключ будет выглядеть так:**
```
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

#### C. VK API (5 минут)

```bash
# 1. Открыть
https://vk.com/dev/access_token

# 2. Создать приложение
# https://vk.com/dev/apps?act=manage

# 3. Create Application
# Тип: Standalone
# Название: MULTIC-Scout

# 4. Settings → Tokens → Create Server Token
# Права: video, groups
# Скопировать token
```

**Ключ будет выглядеть так:**
```
VK_API_TOKEN=vk1.a.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

#### D. (Опционально) Twitter API

Если нужен мониторинг трендов:

```bash
https://developer.twitter.com/
# Создать приложение
# Скопировать Bearer Token
```

---

### Шаг 2️⃣: Создать .env Файл (2 минуты)

Создать файл `multic/.env`:

```bash
# ⭐ ОБЯЗАТЕЛЬНЫЕ
BRAVE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VK_API_TOKEN=vk1.a.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VK_API_VERSION=5.131

# 📱 ОПЦИОНАЛЬНО
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAAAAxx

# 🗄️ БД
DATABASE_PATH=./scout_db.sqlite

# ⏱️ РАСПИСАНИЕ
SEARCH_INTERVAL_HOURS=1
```

**⚠️ ВАЖНО:** Добавить `.env` в `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

### Шаг 3️⃣: Установить Зависимости (10 минут)

#### A. Создать requirements.txt

```bash
# scout-agent/requirements.txt

requests>=2.28.0
beautifulsoup4>=4.11.0
python-dotenv>=0.20.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.80.0
vk-api>=11.9.0
aiohttp>=3.8.0
```

#### B. Установить

```bash
# Перейти в проект
cd path/to/multic

# Установить зависимости
pip install -r scout-agent/requirements.txt

# Проверить
python -c "import requests; print('✅ OK')"
```

---

### Шаг 4️⃣: Создать Первый Скрипт (30 минут)

#### A. Создать файл `scout_test.py`

```python
# scout_test.py

import os
from dotenv import load_dotenv
import requests

# Загрузить переменные окружения
load_dotenv()

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
VK_API_TOKEN = os.getenv("VK_API_TOKEN")

def test_brave_search():
    """Тест Brave Search API"""
    print("\n1️⃣ Тестируем Brave Search...")
    
    headers = {"Authorization": f"Bearer {BRAVE_API_KEY}"}
    params = {
        "q": "славяно-арийская культура видео",
        "count": 10
    }
    
    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        print("✅ Brave Search работает!")
        results = response.json()
        print(f"   Найдено результатов: {len(results.get('web', []))}")
        
        # Показать первые 3 результата
        for i, result in enumerate(results.get('web', [])[:3], 1):
            print(f"   {i}. {result['title'][:50]}...")
        
        return True
    else:
        print(f"❌ Ошибка {response.status_code}: {response.text}")
        return False

def test_youtube_search():
    """Тест YouTube API"""
    print("\n2️⃣ Тестируем YouTube Search...")
    
    try:
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.search().list(
            q="славяно-арийская культура",
            part='snippet',
            maxResults=5,
            type='video'
        )
        
        response = request.execute()
        
        print("✅ YouTube API работает!")
        print(f"   Найдено видео: {len(response.get('items', []))}")
        
        # Показать первые 3 видео
        for i, item in enumerate(response.get('items', [])[:3], 1):
            title = item['snippet']['title']
            print(f"   {i}. {title[:50]}...")
        
        return True
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_vk_search():
    """Тест VK API"""
    print("\n3️⃣ Тестируем VK API...")
    
    try:
        import vk_api
        
        vk = vk_api.VkApi(token=VK_API_TOKEN, api_version="5.131")
        
        results = vk.method('video.search', {
            'q': 'славяно-арийская культура',
            'count': 5,
            'sort': 1
        })
        
        print("✅ VK API работает!")
        print(f"   Найдено видео: {len(results.get('items', []))}")
        
        # Показать первые 3 видео
        for i, video in enumerate(results.get('items', [])[:3], 1):
            print(f"   {i}. {video['title'][:50]}...")
        
        return True
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Главная функция"""
    print("=" * 60)
    print("ТЕСТ SCOUT AGENT")
    print("=" * 60)
    
    results = {
        "Brave": test_brave_search(),
        "YouTube": test_youtube_search(),
        "VK": test_vk_search()
    }
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    for api, status in results.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {api}")
    print("=" * 60)
    
    all_ok = all(results.values())
    if all_ok:
        print("\n🎉 ВСЕ API РАБОТАЮТ!")
        return 0
    else:
        print("\n⚠️ Некоторые API не работают. Проверьте ключи.")
        return 1

if __name__ == "__main__":
    exit(main())
```

#### B. Запустить тест

```bash
python scout_test.py
```

**Ожидаемый результат:**

```
============================================================
ТЕСТ SCOUT AGENT
============================================================

1️⃣ Тестируем Brave Search...
✅ Brave Search работает!
   Найдено результатов: 10
   1. Славяно-арийская культура: история...
   2. Наследие славян: древние корни...
   3. История славянства: видео...

2️⃣ Тестируем YouTube Search...
✅ YouTube API работает!
   Найдено видео: 5
   1. История славян - документальный фильм
   2. Славяно-арийская культура - полный курс
   3. Древние славяне: наследие предков

3️⃣ Тестируем VK API...
✅ VK API работает!
   Найдено видео: 5
   1. Славяно-арийская культура [ВК]
   2. История славян из архивов
   3. Традиции наших предков

============================================================
РЕЗУЛЬТАТЫ:
✅ Brave
✅ YouTube
✅ VK
============================================================

🎉 ВСЕ API РАБОТАЮТ!
```

---

### Шаг 5️⃣: Создать Первый Scout Скрипт (30 минут)

#### A. Создать `scout_find_videos.py`

```python
# scout_find_videos.py

import os
from dotenv import load_dotenv
import requests
from googleapiclient.discovery import build
import vk_api

load_dotenv()

class ScoutAgent:
    """Простая версия Scout Agent"""
    
    def __init__(self):
        self.brave_key = os.getenv("BRAVE_API_KEY")
        self.youtube_key = os.getenv("YOUTUBE_API_KEY")
        self.vk_token = os.getenv("VK_API_TOKEN")
        self.youtube = build('youtube', 'v3', developerKey=self.youtube_key)
    
    def find_viral_videos(self, topic, min_views=50000, limit=5):
        """Найти вирусные видео"""
        
        print(f"\n🔍 Поиск видео по теме: {topic}")
        print(f"   Минимум просмотров: {min_views:,}")
        print(f"   Лимит результатов: {limit}")
        
        all_videos = []
        
        # 1. YouTube поиск
        print("\n   📺 Поиск на YouTube...")
        yt_videos = self._search_youtube(topic, min_views)
        all_videos.extend(yt_videos)
        print(f"      Найдено: {len(yt_videos)}")
        
        # 2. VK поиск
        print("   📱 Поиск в ВКонтакте...")
        vk_videos = self._search_vk(topic, min_views)
        all_videos.extend(vk_videos)
        print(f"      Найдено: {len(vk_videos)}")
        
        # 3. Сортировка по просмотрам
        all_videos.sort(key=lambda x: x['views'], reverse=True)
        
        # 4. Вернуть ТОП
        top_videos = all_videos[:limit]
        
        return top_videos
    
    def _search_youtube(self, query, min_views):
        """Поиск на YouTube"""
        
        request = self.youtube.search().list(
            q=query,
            part='snippet',
            maxResults=50,
            type='video',
            order='viewCount'
        )
        
        response = request.execute()
        videos = []
        
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            
            # Получить статистику
            stats_request = self.youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            )
            
            stats_response = stats_request.execute()
            if stats_response['items']:
                video_data = stats_response['items'][0]
                
                views = int(video_data['statistics'].get('viewCount', 0))
                if views >= min_views:
                    videos.append({
                        'title': video_data['snippet']['title'],
                        'url': f"https://youtube.com/watch?v={video_id}",
                        'views': views,
                        'likes': int(video_data['statistics'].get('likeCount', 0)),
                        'comments': int(video_data['statistics'].get('commentCount', 0)),
                        'platform': 'YouTube'
                    })
        
        return videos
    
    def _search_vk(self, query, min_views):
        """Поиск в ВКонтакте"""
        
        try:
            vk = vk_api.VkApi(token=self.vk_token, api_version="5.131")
            
            results = vk.method('video.search', {
                'q': query,
                'count': 50,
                'sort': 1
            })
            
            videos = []
            for video in results.get('items', []):
                videos.append({
                    'title': video['title'],
                    'url': f"https://vk.com/video{video['owner_id']}_{video['id']}",
                    'views': video.get('views', 0),
                    'likes': video.get('likes', 0),
                    'comments': video.get('comments', 0),
                    'platform': 'VKontakte'
                })
            
            return videos
        
        except Exception as e:
            print(f"      ❌ Ошибка VK: {e}")
            return []
    
    def print_results(self, videos):
        """Вывести результаты"""
        
        print("\n" + "=" * 70)
        print("🏆 ТОПОВЫЕ ВИРУСНЫЕ ВИДЕО")
        print("=" * 70)
        
        for i, video in enumerate(videos, 1):
            engagement = (video['likes'] + video['comments']) / video['views'] * 100 if video['views'] > 0 else 0
            
            print(f"\n#{i} {video['platform']}")
            print(f"   Название: {video['title']}")
            print(f"   URL: {video['url']}")
            print(f"   Просмотры: {video['views']:,}")
            print(f"   Лайки: {video['likes']:,}")
            print(f"   Комментарии: {video['comments']:,}")
            print(f"   Engagement: {engagement:.2f}%")
        
        print("\n" + "=" * 70)

def main():
    """Главная функция"""
    
    scout = ScoutAgent()
    
    # Найти видео
    videos = scout.find_viral_videos(
        topic="славяно-арийская культура",
        min_views=50000,
        limit=5
    )
    
    # Вывести результаты
    scout.print_results(videos)

if __name__ == "__main__":
    main()
```

#### B. Запустить

```bash
python scout_find_videos.py
```

---

## 📚 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ

### Где узнать больше?

1. **SCOUT_AGENT_ARCHITECTURE.md** — Полная архитектура
2. **SCOUT_AGENT_SKILLS.md** — Встроенные скиллы Claude
3. **SCOUT_AGENT_API_SETUP.md** — Подробная настройка
4. **SCOUT_AGENT_INTEGRATION.md** — Интеграция с MULTIC

### Полезные ссылки

- [Brave Search API Docs](https://api.search.brave.com/res/v1/docs)
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [VK API Docs](https://vk.com/dev/methods)
- [Python Requests](https://requests.readthedocs.io/)

### Коман полезные команды

```bash
# Тест всех API
python scout_test.py

# Поиск вирусных видео
python scout_find_videos.py

# Просмотр .env
cat .env

# Проверить установку
pip list | grep -E "requests|google|vk-api"
```

---

## ❓ КОГДА ЧТО-ТО ПОШЛО НЕ ТАК

### Ошибка: "ModuleNotFoundError: No module named 'requests'"

```bash
pip install requests
```

### Ошибка: "401 Unauthorized" (Brave)

```
Проверить BRAVE_API_KEY в .env
Убедиться что ключ скопирован правильно
```

### Ошибка: "API key not valid" (YouTube)

```
Убедиться что YouTube Data API v3 включена
Перейти в console.developers.google.com
Включить API
```

### Ошибка: "Invalid token" (VK)

```
Проверить VK_API_TOKEN в .env
Убедиться что указана версия API (5.131)
```

---

## ✅ ЧЕК-ЛИСТ

```
☐ Получены 3 API ключа (Brave, YouTube, VK)
☐ Создан .env файл с ключами
☐ Добавлен .env в .gitignore
☐ Установлены зависимости (pip install)
☐ Запущен scout_test.py (все ✅)
☐ Запущен scout_find_videos.py
☐ Видео найдены и выведены ✅

ГОТОВО! 🎉
```

---

**Время:** 30-60 минут от начала до первого поиска  
**Стоимость:** $0 USD  
**Результат:** Рабочий Scout Agent! ✅

🚀 **Готовы? Начинайте с Шага 1!**

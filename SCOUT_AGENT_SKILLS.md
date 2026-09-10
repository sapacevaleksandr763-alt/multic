# 🎯 SCOUT AGENT - Скиллы и Возможности

**Версия:** 1.0  
**Дата:** 2026-09-10  
**Агент:** Scout / Researcher (7-й агент MULTIC)

---

## 📚 ВСТРОЕННЫЕ СКИЛЛЫ CLAUDE

### Скилл 1️⃣: `/investigate` (gstack)

**Назначение:** Расследование и глубокий анализ  
**Тип:** Встроенный скилл gstack  
**Использование:** Когда нужно выяснить причину и провести детальный анализ

#### Примеры использования:

```
/investigate "почему видео стало вирусным"
/investigate "какие факторы влияют на вирусность"
/investigate "анализ тренда [название]"
```

#### В коде Scout Agent:

```python
class ScoutAgent:
    def deep_analysis(self, topic, data):
        """Использует /investigate для глубокого анализа"""
        result = self.claude_client.investigate(
            question=f"Почему {topic} стало популярным?",
            evidence=data,
            depth="comprehensive"
        )
        return result
    
    def analyze_virality_factors(self, video_data):
        """Исследует факторы виральности видео"""
        analysis = self.investigate(
            f"Факторы виральности видео: {video_data['title']}",
            {
                'views': video_data['views'],
                'likes': video_data['likes'],
                'comments': video_data['comments'],
                'engagement_rate': video_data['engagement_rate']
            }
        )
        return analysis
```

---

### Скилл 2️⃣: `investigate` (встроенный)

**Назначение:** Открытая разведка и исследование  
**Тип:** Встроенный скилл Claude  
**Использование:** Основной скилл для поиска информации и разведки

#### Примеры использования:

```
investigate "лучшие видео по теме Славяно-арийская культура"
investigate "популярные каналы в нише истории"
investigate "тренды в видеоконтенте 2026"
```

#### В коде Scout Agent:

```python
class ScoutAgent:
    def research_topic(self, topic, niche):
        """Основной метод для разведки информации"""
        research_results = self.investigate(
            topic=topic,
            context=niche,
            sources="web + social media"
        )
        return research_results
    
    def find_viral_videos(self, niche):
        """Находит вирусные видео в нише"""
        videos = self.investigate(
            f"Найти 5 лучших вирусных видео в нише: {niche}",
            search_sources=["youtube", "vk", "instagram", "tiktok"]
        )
        return videos
    
    def monitor_trends(self, topic):
        """Мониторит тренды по теме"""
        trends = self.investigate(
            f"Актуальные тренды: {topic}",
            timeframe="last_7_days"
        )
        return trends
```

---

### Скилл 3️⃣: `content-research-writer`

**Назначение:** Исследовательское письмо с поиском источников  
**Тип:** Встроенный скилл для аналитических отчетов  
**Использование:** Создание отчетов с ссылками на источники

#### Примеры использования:

```
content-research-writer "Анализ вирусных видео в нише культуры"
content-research-writer "Отчет о трендах социальных сетей"
```

#### В коде Scout Agent:

```python
class ScoutAgent:
    def generate_analysis_report(self, videos_data, topic):
        """Генерирует аналитический отчет с источниками"""
        report = self.content_research_writer(
            topic=f"Анализ вирусных видео: {topic}",
            research_data=videos_data,
            include_sources=True,
            format="markdown"
        )
        return report
    
    def create_virality_report(self, videos_list):
        """Создает отчет о факторах виральности"""
        report = self.content_research_writer(
            topic="Факторы виральности видеороликов",
            research_data={
                'videos': videos_list,
                'analysis': self.analyze_metrics(videos_list)
            },
            include_citations=True
        )
        return report
    
    def write_trend_analysis(self, trend_data):
        """Пишет анализ трендов с источниками"""
        analysis = self.content_research_writer(
            topic="Анализ текущих трендов",
            research_data=trend_data,
            citation_style="markdown"
        )
        return analysis
```

---

### Скилл 4️⃣: `browse` (встроенный)

**Назначение:** Быстрый браузинг конкретных сайтов  
**Тип:** Встроенный скилл Claude  
**Использование:** Открытие и чтение конкретных URL

#### Примеры использования:

```
browse "https://youtube.com/@channel"
browse "https://vk.com/video"
browse "https://example.com/article"
```

#### В коде Scout Agent:

```python
class ScoutAgent:
    def check_url(self, url):
        """Открывает и анализирует конкретную страницу"""
        content = self.browse(url)
        return content
    
    def scrape_youtube_channel(self, channel_url):
        """Получает информацию с YouTube канала"""
        page_content = self.browse(channel_url)
        # Парсит информацию о видео
        return self.parse_youtube_data(page_content)
    
    def analyze_website(self, url):
        """Анализирует содержимое сайта"""
        content = self.browse(url)
        analysis = {
            'title': self.extract_title(content),
            'description': self.extract_description(content),
            'links': self.extract_links(content),
            'images': self.extract_images(content)
        }
        return analysis
    
    def get_article_content(self, url):
        """Получает полный текст статьи"""
        article = self.browse(url)
        return {
            'title': self.extract_title(article),
            'content': self.extract_main_content(article),
            'author': self.extract_author(article),
            'date': self.extract_date(article)
        }
```

---

## 🔌 ВНЕШНИЕ API И ИНСТРУМЕНТЫ

### API 1️⃣: Brave Search API ⭐ ГЛАВНЫЙ

**Назначение:** Основной веб-поиск  
**Получение ключа:** https://brave.com/search/api (бесплатно)  
**Лимит:** 2000 запросов/день  

#### Использование в коде:

```python
import requests

class BraveSearchClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def search(self, query, count=10):
        """Основной поиск через Brave"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"q": query, "count": count}
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()
    
    def search_videos(self, query):
        """Поиск видео через Brave"""
        results = self.search(f"{query} video", count=20)
        return self.filter_videos(results)
    
    def search_news(self, query):
        """Поиск новостей"""
        results = self.search(f"{query} news", count=10)
        return self.filter_news(results)

# Использование:
brave = BraveSearchClient(os.getenv("BRAVE_API_KEY"))
videos = brave.search_videos("славяно-арийская культура")
```

---

### API 2️⃣: YouTube Data API

**Назначение:** Поиск видео, получение статистики  
**Получение:** https://console.developers.google.com/  
**Лимит:** 10,000 запросов/день  

#### Использование в коде:

```python
from googleapiclient.discovery import build

class YouTubeClient:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos(self, query, max_results=50):
        """Поиск видео на YouTube"""
        request = self.youtube.search().list(
            q=query,
            part='snippet',
            maxResults=max_results,
            type='video',
            order='viewCount'  # Сортировка по просмотрам
        )
        response = request.execute()
        return response['items']
    
    def get_video_stats(self, video_id):
        """Получить статистику видео"""
        request = self.youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        )
        response = request.execute()
        video = response['items'][0]
        return {
            'title': video['snippet']['title'],
            'views': int(video['statistics'].get('viewCount', 0)),
            'likes': int(video['statistics'].get('likeCount', 0)),
            'comments': int(video['statistics'].get('commentCount', 0))
        }
    
    def find_viral_videos(self, query, min_views=100000):
        """Находит вирусные видео (>100k просмотров)"""
        videos = self.search_videos(query)
        viral_videos = []
        for video in videos:
            stats = self.get_video_stats(video['id']['videoId'])
            if stats['views'] >= min_views:
                viral_videos.append(stats)
        return viral_videos

# Использование:
youtube = YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
viral = youtube.find_viral_videos("славяно-арийская культура", min_views=50000)
```

---

### API 3️⃣: VK API (ВКонтакте)

**Назначение:** Поиск видео в ВКонтакте  
**Получение:** https://vk.com/dev/access_token  
**Лимит:** 3 запроса/сек  

#### Использование в коде:

```python
import vk_api

class VKClient:
    def __init__(self, access_token):
        self.vk = vk_api.VkApi(token=access_token)
    
    def search_videos(self, query, count=50):
        """Поиск видео в ВКонтакте"""
        results = self.vk.method('video.search', {
            'q': query,
            'count': count,
            'sort': 1  # Сортировка по популярности
        })
        return results['items']
    
    def search_group_videos(self, group_id, count=100):
        """Получить видео из группы"""
        results = self.vk.method('video.get', {
            'owner_id': f"-{group_id}",
            'count': count,
            'sort': 0  # Новые первыми
        })
        return results['items']
    
    def get_group_info(self, group_id):
        """Информация о группе"""
        info = self.vk.method('groups.getById', {
            'group_id': group_id,
            'fields': 'members_count,description'
        })
        return info[0]

# Использование:
vk = VKClient(os.getenv("VK_API_TOKEN"))
videos = vk.search_videos("славяно-арийская культура", count=100)
```

---

### API 4️⃣: Wikimedia Commons

**Назначение:** Поиск изображений  
**Использование:** Полностью бесплатно  

#### Использование в коде:

```python
import mediawiki

class WikimediaClient:
    def search_images(self, query, limit=50):
        """Поиск изображений в Wikimedia"""
        results = []
        # Поиск через Wikimedia API
        # ...
        return results
```

---

### API 5️⃣: Twitter/X API (опционально)

**Назначение:** Мониторинг трендов  
**Бесплатный уровень:** Ограничен  

---

## 🔄 ИНТЕГРАЦИЯ СКИЛЛОВ

### Основной workflow Scout Agent:

```python
class ScoutAgent:
    def execute_research_task(self, task_type, query):
        """Главный метод исследования"""
        
        if task_type == "find_viral_videos":
            # Шаг 1: Использовать investigate для поиска
            initial_search = self.investigate(
                f"Лучшие вирусные видео: {query}"
            )
            
            # Шаг 2: Собрать видео через API
            videos = self.gather_video_data(query)
            
            # Шаг 3: Использовать /investigate для анализа
            analysis = self.scout_client.investigate(
                "Факторы виральности",
                videos
            )
            
            # Шаг 4: Создать отчет через content-research-writer
            report = self.content_research_writer(
                f"Анализ вирусных видео: {query}",
                {
                    'videos': videos,
                    'analysis': analysis
                }
            )
            
            return report
        
        elif task_type == "monitor_trends":
            # Мониторинг трендов
            trends = self.investigate(f"Актуальные тренды: {query}")
            return trends
        
        elif task_type == "analyze_competitor":
            # Анализ конкурента
            competitor_data = self.browse(query)  # URL конкурента
            analysis = self.analyze_website_content(competitor_data)
            return analysis
```

---

## 📊 ПРИМЕРЫ ВЫВОДА

### Пример 1: Результат поиска вирусных видео

```json
{
  "status": "success",
  "task": "find_viral_videos",
  "query": "славяно-арийская культура",
  "videos_found": 5,
  "videos": [
    {
      "id": "video_001",
      "title": "История славян",
      "author": "Channel Name",
      "url": "https://youtube.com/watch?v=...",
      "views": 1250000,
      "likes": 45000,
      "comments": 12000,
      "engagement_rate": "4.57%",
      "virality_factors": [
        "Редкая историческая информация",
        "Профессиональное оформление",
        "Активное сообщество",
        "Актуальная тема"
      ]
    }
    // ... еще 4 видео
  ],
  "analysis": {
    "average_views": 950000,
    "average_engagement": "3.8%",
    "common_factors": [
      "Образовательный контент",
      "Высокое качество видео",
      "Активные комментарии"
    ]
  }
}
```

---

## ✅ СТАТУС СКИЛЛОВ

| Скилл | Статус | Использование |
|-------|--------|----------------|
| `/investigate` | ✅ Готов | Глубокий анализ |
| `investigate` | ✅ Готов | Основной поиск |
| `content-research-writer` | ✅ Готов | Отчеты |
| `browse` | ✅ Готов | Чтение сайтов |
| Brave Search API | ✅ Готов | Веб-поиск |
| YouTube Data API | ✅ Готов | Видеоролики |
| VK API | ✅ Готов | ВКонтакте |
| Wikimedia Commons | ✅ Готов | Изображения |
| Twitter/X API | ⏳ Опционально | Тренды |

---

**Версия:** 1.0  
**Статус:** ✅ Полностью готов к использованию  
**Дата обновления:** 2026-09-10

🚀 **Scout Agent готов с полным набором скиллов!**

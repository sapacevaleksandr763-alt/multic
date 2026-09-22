# Agent-Reach Integration - MULTIC Phase 2C+

## Обзор

**Agent-Reach** интегрирован в систему MULTIC для мониторинга социальных сетей, анализа трендов и отслеживания конкурентов.

**Установка:** https://github.com/Panniantong/Agent-Reach

---

## 📍 Архитектура

```
AgentReachMonitor (agent_reach_monitor.py)
├── search_trends()              → Поиск трендов (Reddit, YouTube, GitHub, X)
├── monitor_competitors()        → Мониторинг конкурентов
├── extract_video_metadata()     → Извлечение метаданных видео
└── get_trending_hashtags()      → Тренды хэштегов

TrendAnalyzer (trend_analyzer.py)
├── analyze_trends()             → Анализ текущих трендов
├── analyze_competitor_strategy()→ Анализ стратегии конкурентов
└── generate_content_strategy()  → Рекомендации для контента

PromotionWorkflow (workflow.py)
└── reach_monitor: AgentReachMonitor  → Интегрирован в основной workflow
```

---

## 🎯 Функциональность

### 1. **Поиск трендов** (search_trends)

```python
trends = monitor.search_trends(keywords=["Славянская культура"])
# Результат:
# {
#     "reddit": [TrendData(...), ...],
#     "youtube": [TrendData(...), ...],
#     "x_twitter": [TrendData(...), ...],
#     "github": [TrendData(...), ...],
# }
```

**Используется в:** Scout Agent → обогащение поиска видео трендовыми топиками

---

### 2. **Мониторинг конкурентов** (monitor_competitors)

```python
posts = monitor.monitor_competitors(["Конкурент1", "Конкурент2"])
# Результат:
# {
#     "youtube": [CompetitorPost(...), ...],
#     "x_twitter": [CompetitorPost(...), ...],
#     "reddit": [CompetitorPost(...), ...],
# }
```

**Используется в:** Dashboard Agent → отслеживание конкурентных стратегий

---

### 3. **Извлечение метаданных видео** (extract_video_metadata)

```python
metadata = monitor.extract_video_metadata(
    "https://youtube.com/watch?v=...",
    platform="youtube"
)
# Результат:
# VideoMetadata(
#     video_id="...",
#     title="...",
#     duration_seconds=120,
#     views=1000,
#     transcript="...",  # Из Whisper API
#     subtitles="...",   # Из платформы
# )
```

**Используется в:** Phase 2A → улучшение анализа видео (субтитры, стенограммы)

---

### 4. **Анализ трендов** (TrendAnalyzer)

```python
analyzer = TrendAnalyzer(monitor)

# Анализ текущих трендов
trends = analyzer.analyze_trends()
# TrendAnalysis(
#     trending_keywords=[("keyword", 0.9), ...],
#     trending_hashtags=[("#tag", 100), ...],
#     trending_formats=[("short_video", 0.85), ...],
#     optimal_posting_times={"youtube": "18:00", ...},
#     virality_factors={"hook": 0.8, ...},
# )

# Анализ конкурентов
competitor_analysis = analyzer.analyze_competitor_strategy(["Comp1"])

# Рекомендуемая стратегия контента
strategy = analyzer.generate_content_strategy(trends, competitor_analysis)
# ContentStrategy(
#     primary_themes=["тема1", "тема2"],
#     recommended_hashtags=["#tag1", "#tag2"],
#     optimal_platforms=["youtube", "telegram"],
#     posting_schedule={"youtube": "18:00"},
#     hook_suggestions=["Как это работает...", ...],
#     content_gaps=["ниша1", "ниша2"],
# )
```

---

## 🔌 Интеграционные точки

### Phase 2A: Scout Agent
**Функция:** Обогащение поиска видео трендовыми данными

```python
# В video_finder.py
from promotion_agent.agent_reach_monitor import AgentReachMonitor

class VideoFinder:
    def __init__(self, config):
        self.monitor = AgentReachMonitor(config)
    
    def search_all_platforms(self):
        # 1. Получить текущие тренды
        trends = self.monitor.search_trends()
        
        # 2. Использовать тренды для поиска
        # - Приоритизировать видео с трендовыми ключевыми словами
        # - Добавить оценку виральности на основе тренда
        # - Фильтровать видео по трендовым форматам
```

---

### Phase 2C: Promotion Agent
**Функция:** Стратегия публикации на основе трендов

```python
# В workflow.py
class PromotionWorkflow:
    def discover_videos(self):
        # Получить тренды перед публикацией
        trends = self.reach_monitor.analyze_trends()
        
        # Использовать тренды для выбора платформ публикации
        # Оптимизировать время публикации
        # Выбрать рекомендуемые хэштеги
```

---

### Phase 2D: Master Dashboard
**Функция:** Мониторинг конкурентов и трендов в реальном времени

```python
# В dashboard_agent/api.py
class DashboardAPI:
    def get_competitive_analysis(self):
        # Получить данные о конкурентах
        competitors = self.reach_monitor.monitor_competitors(competitor_names)
        
        # Вернуть анализ в Dashboard
        return {
            "competitor_posts": len(competitors),
            "average_engagement": ...,
            "underexploited_platforms": ...,
            "content_gaps": ...,
        }
```

---

## 📊 Типы данных

### TrendData
```python
@dataclass
class TrendData:
    platform: str               # "reddit", "youtube", "x_twitter", "github"
    title: str                  # Заголовок тренда
    content: str                # Описание контента
    engagement_count: int       # Количество взаимодействий
    timestamp: datetime         # Когда обнаружен тренд
    url: str                    # Ссылка на контент
    source: str                 # Источник (YouTube, Reddit, etc)
    score: float                # Оценка виральности (0-100)
```

### CompetitorPost
```python
@dataclass
class CompetitorPost:
    platform: str               # Платформа публикации
    competitor_name: str        # Имя конкурента
    post_id: str                # ID поста
    content: str                # Текст контента
    views: int                  # Количество просмотров
    engagement: int             # Лайки + комментарии + репосты
    timestamp: datetime         # Время публикации
    url: str                    # Ссылка на пост
    tags: List[str]             # Хэштеги / теги
    engagement_rate: float      # Рейт взаимодействия (%)
```

### VideoMetadata
```python
@dataclass
class VideoMetadata:
    video_id: str               # ID видео
    title: str                  # Название
    platform: str               # Платформа
    duration_seconds: int       # Длительность в секундах
    views: int                  # Просмотры
    engagement: int             # Взаимодействия
    transcript: Optional[str]   # Стенограмма (из Whisper)
    subtitles: Optional[str]    # Субтитры
    key_moments: Optional[List] # Ключевые моменты видео
```

---

## 🚀 Использование

### Запуск мониторинга трендов

```python
from promotion_agent.config import PromotionConfig
from promotion_agent.agent_reach_monitor import AgentReachMonitor
from promotion_agent.trend_analyzer import TrendAnalyzer

# Инициализация
config = PromotionConfig.from_env()
monitor = AgentReachMonitor(config)
analyzer = TrendAnalyzer(monitor)

# Анализ трендов
trends = analyzer.analyze_trends()
print(f"Тренды: {trends.trending_keywords}")

# Анализ конкурентов
comp_analysis = analyzer.analyze_competitor_strategy(["Конкурент1"])
print(f"Стратегия конкурентов: {comp_analysis}")

# Рекомендации контента
strategy = analyzer.generate_content_strategy(trends, comp_analysis)
print(f"Рекомендуемые платформы: {strategy.optimal_platforms}")
print(f"Оптимальное время: {strategy.posting_schedule}")
```

---

## 📝 TODO: Реализация API интеграций

Каждый метод с `TODO:` требует реальной интеграции с API:

| Метод | Платформа | API | Статус |
|-------|-----------|-----|--------|
| `_search_reddit_trends()` | Reddit | PRAW | ⏳ TODO |
| `_search_youtube_trends()` | YouTube | YouTube Data API | ⏳ TODO |
| `_search_x_trends()` | X/Twitter | Tweepy | ⏳ TODO |
| `_search_github_trends()` | GitHub | GitHub API | ⏳ TODO |
| `_monitor_youtube_channels()` | YouTube | YouTube Data API | ⏳ TODO |
| `_monitor_x_accounts()` | X/Twitter | Tweepy | ⏳ TODO |
| `_monitor_reddit_communities()` | Reddit | PRAW | ⏳ TODO |
| `_get_transcript()` | All | Whisper API | ⏳ TODO |
| `_get_subtitles()` | Video | Platform API | ⏳ TODO |

---

## 🔑 Требуемые ключи API

```env
# Существующие
YOUTUBE_API_KEY=...
TELEGRAM_BOT_TOKEN=...
CLAUDE_API_KEY=...

# Для Agent-Reach интеграции
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=...

X_API_KEY=...
X_API_SECRET=...
X_BEARER_TOKEN=...

GITHUB_TOKEN=...
```

---

## 📚 Документация Agent-Reach

- **GitHub:** https://github.com/Panniantong/Agent-Reach
- **Функциональность:**
  - Reddit поиск и мониторинг
  - YouTube API интеграция
  - X/Twitter API интеграция
  - GitHub trends анализ
  - Извлечение субтитров из видео
  - Анализ комментариев и отзывов

---

## 🎯 Следующие шаги

1. ✅ **Архитектура модулей** - DONE
2. ✅ **Типы данных и интерфейсы** - DONE
3. ✅ **Тестовое покрытие (36 тестов)** - DONE
4. ⏳ **API интеграции** - когда готовы ключи
5. ⏳ **Интеграция в Phase 2A/2C/2D** - после API
6. ⏳ **Dashboard визуализация** - последний этап

---

## 💬 Примеры использования

### Пример 1: Поиск трендов перед публикацией

```python
# В workflow.py перед публикацией
def publish_videos(self):
    # Получить тренды
    trends = self.reach_monitor.analyze_trends()
    
    # Выбрать видео с трендовыми ключевыми словами
    videos_to_publish = [
        v for v in self.db.get_approved_videos()
        if any(kw in v.title for kw, _ in trends.trending_keywords[:5])
    ]
    
    # Опубликовать с оптимальным временем
    for video in videos_to_publish:
        best_time = trends.optimal_posting_times.get("youtube", "18:00")
        self.publishers["youtube"].publish(video, scheduled_time=best_time)
```

### Пример 2: Анализ конкурентов

```python
# В dashboard
competitor_analysis = monitor.analyze_competitor_strategy(
    ["Конкурент1", "Конкурент2"]
)

# Найти незанятые ниши
gaps = competitor_analysis["content_gaps"]
print(f"Возможности: {gaps}")

# Выбрать недостаточно используемые платформы
underexploited = competitor_analysis["underexploited_platforms"]
print(f"Платформы для экспансии: {underexploited}")
```

---

**Статус:** ✅ Architecture complete, API integration pending  
**Дата:** 2026-09-22

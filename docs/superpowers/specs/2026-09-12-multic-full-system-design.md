# MULTIC Multi-Agent System - Full Design Document

**Дата:** 2026-09-12  
**Версия:** 1.0  
**Статус:** Design Phase Complete  
**Автор:** Claude AI + Alex

---

## 📋 Table of Contents

1. Executive Summary
2. Project Scope & Goals
3. Architecture Overview
4. Core Components
5. Agent Specifications (All 15)
6. Data Models
7. Integration Points
8. Workflow Execution
9. Development Phases
10. Deployment Strategy

---

## 1️⃣ EXECUTIVE SUMMARY

**MULTIC** - это полностью автоматизированная система для поиска, анализа и масштабирования вирусного контента в нише Славяно-Арийской культуры.

**Основная задача:** Преобразовать вирусные видео → трафик → Telegram подписчики → продажи товаров/услуг.

**Ключевые метрики:**
- 320,000+ views/месяц
- 1,600+ новых Telegram сubs/месяц
- $8,500+ доход/месяц (месяц 1)
- ROI > 500%

**Архитектура:** 15 специализированных агентов, работающих в едином workflow.

---

## 2️⃣ PROJECT SCOPE & GOALS

### Scope

**✅ Включено в проект:**
- 15 полнофункциональных агентов
- Hybrid архитектура (функции + event-driven)
- CLI, REST API, Telegram Bot интеграция
- SQLite (dev) + PostgreSQL (prod)
- Config-based API интеграция
- Full workflow automation

**❌ НЕ включено:**
- Веб-интерфейс (админ-панель) - может быть позже
- Mobile приложение - может быть позже
- Machine Learning модели - используем готовые API'ы
- Kubernetes оркестрация - не нужна для MVP

### Goals

**Финансовые:**
- Месяц 1: $8,500 доход
- Месяц 2-3: $17,000 доход (2x)
- После автоматизации: $34,000 доход (4x)

**Технические:**
- Все 15 агентов разработаны и протестированы
- Full-cycle workflow работает без ошибок
- System готов к масштабированию

**Timeline:**
- Фаза 1 (недели 1-2): Разработка всех агентов
- Фаза 2 (неделя 3): Интеграция и тестирование
- Фаза 3 (неделя 4): Deployment и оптимизация

---

## 3️⃣ ARCHITECTURE OVERVIEW

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                           │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │   CLI Tool   │  REST API    │   Telegram Bot           │ │
│  │  (commands)  │  (FastAPI)   │   (Real-time control)   │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└────────────────────────┬──────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────┐
│                   EVENT BUS & ORCHESTRATION                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Event Bus (Sync for now, can be async with Celery)     │ │
│  │  - Workflow Coordinator                                 │ │
│  │  - Event Router                                         │ │
│  │  - Error Handler                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└────────────┬──────────────────────────────────────┬───────────┘
             │                                      │
    ┌────────▼────────┐                  ┌─────────▼────────┐
    │  DATA LAYER     │                  │  AGENT LAYER     │
    │ ┌─────────────┐ │                  │ ┌──────────────┐ │
    │ │  Database   │ │                  │ │ 15 Agents    │ │
    │ │ (SQLite/PG) │ │                  │ │ (Python)     │ │
    │ ├─────────────┤ │                  │ ├──────────────┤ │
    │ │  Models:    │ │                  │ │ Content:     │ │
    │ │ - Videos    │ │                  │ │ - Scout      │ │
    │ │ - Analysis  │ │                  │ │ - Copywriter │ │
    │ │ - Campaigns │ │                  │ │ - Vid Editor │ │
    │ │ - Emails    │ │                  │ │              │ │
    │ │ - Sales     │ │                  │ │ Publishing:  │ │
    │ │ - Workflows │ │                  │ │ - Promotion  │ │
    │ └─────────────┘ │                  │ │ - Community  │ │
    │                 │                  │ │              │ │
    │                 │                  │ │ Conversion:  │ │
    │                 │                  │ │ - Email      │ │
    │                 │                  │ │ - Sales      │ │
    │                 │                  │ │              │ │
    │                 │                  │ │ Intelligence:│ │
    │                 │                  │ │ - Audience   │ │
    │                 │                  │ │ - Analytics  │ │
    │                 │                  │ │ - A/B Test   │ │
    │                 │                  │ │              │ │
    │                 │                  │ │ System:      │ │
    │                 │                  │ │ - Manager    │ │
    │                 │                  │ │ - Strategist │ │
    │                 │                  │ │ - Trend Ana. │ │
    │                 │                  │ │ - Automation │ │
    │                 │                  │ └──────────────┘ │
    └─────────────────┘                  └──────────────────┘
             │                                      │
             └──────────────┬───────────────────────┘
                            │
        ┌───────────────────▼────────────────────┐
        │    EXTERNAL INTEGRATIONS               │
        │ ┌──────────────────────────────────┐  │
        │ │ Video APIs:                      │  │
        │ │ - YouTube, VK, Instagram,        │  │
        │ │   Trendsee, LiveDune             │  │
        │ │                                  │  │
        │ │ Publishing APIs:                 │  │
        │ │ - TikTok, Instagram, YouTube,    │  │
        │ │   Telegram                       │  │
        │ │                                  │  │
        │ │ Services:                        │  │
        │ │ - Caption App, Mailchimp,        │  │
        │ │   Stripe, Zapier                 │  │
        │ └──────────────────────────────────┘  │
        └────────────────────────────────────────┘
```

### Technology Stack

**Language:** Python 3.11+
**Web Framework:** FastAPI + Pydantic
**Database:** SQLite (dev) → PostgreSQL (prod)
**ORM:** SQLAlchemy
**CLI:** Click
**Telegram:** python-telegram-bot
**Async:** asyncio, httpx
**Testing:** pytest
**Deployment:** Docker + Docker Compose

---

## 4️⃣ CORE COMPONENTS

### 4.1 Event Bus System

```python
# core/event_bus.py

class EventBus:
    """
    Central event routing and coordination system.
    Connects agents through events instead of direct calls.
    """
    
    def publish(self, event_type: str, data: dict) -> None:
        """Publish an event that agents listen to"""
        
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to specific event type"""
        
    def get_event_history(self, workflow_id: str) -> List[Event]:
        """Get all events for a workflow"""
```

**Events (примеры):**
- `scout:videos_found` → Scout нашёл видео
- `analysis:complete` → Анализ завершён
- `copywriting:done` → Промпты созданы
- `video_editing:done` → Видео смонтировано
- `publication:complete` → Видео опубликовано
- `email:sent` → Email отправлены
- `sales:closed` → Сделка закрыта
- `workflow:error` → Ошибка в workflow

### 4.2 Database Layer

```python
# core/database.py

class DatabaseManager:
    """
    Abstraction for SQLite/PostgreSQL.
    One interface, multiple backends.
    """
    
    def __init__(self, config: Config):
        if config.ENV == "development":
            self.db = SQLite("multic.db")
        else:
            self.db = PostgreSQL(config.DATABASE_URL)
    
    def get_session(self):
        """Get SQLAlchemy session"""
        
    def migrate(self):
        """Run migrations"""
```

### 4.3 Config System

```yaml
# config/development.yml
ENVIRONMENT: development
DATABASE: sqlite:///multic.db
LOG_LEVEL: DEBUG

APIS:
  SCOUT:
    USE_YOUTUBE: true
    USE_VK: true
    USE_INSTAGRAM: true
    USE_MOCK: false  # Отключено, используем реальные API'ы
    
  EMAIL:
    PROVIDER: mock  # Используем mock для разработки
    API_KEY: null
    
  SALES:
    PROVIDER: mock
    STRIPE_KEY: null

# config/production.yml
ENVIRONMENT: production
DATABASE: postgresql://...
LOG_LEVEL: INFO

APIS:
  SCOUT:
    USE_YOUTUBE: true
    USE_VK: true
    USE_MOCK: false
    
  EMAIL:
    PROVIDER: mailchimp
    API_KEY: ${MAILCHIMP_API_KEY}
```

---

## 5️⃣ AGENT SPECIFICATIONS (ALL 15)

### Group 1: System & Coordination (4 agents)

#### 1. 🎯 Manager Agent
**Purpose:** Координация всех других агентов, управление workflow  
**Input:** Команда от пользователя  
**Output:** Приказы другим агентам  
**Responsibilities:**
- Получить задачу (найти топ-видео по теме, количество видео)
- Разложить на подзадачи
- Выдать приказы Scout, Strategist, Copywriter, Video Editor, Promotion Manager
- Мониторить статус каждого агента
- Обработать ошибки и переслать
- Доложить результаты

#### 2. 📊 Strategist Agent
**Purpose:** Анализ трендов и разработка стратегии контента  
**Input:** 5 вирусных видео от Scout  
**Output:** Стратегический план (целевая аудитория, факторы виральности, рекомендации)  
**Key Functions:**
- SWOT анализ каждого видео
- Выявление факторов виральности
- Определение целевой аудитории
- Прогноз метрик
- Рекомендации по адаптации

#### 3. 🔥 Trend Analyst Agent
**Purpose:** Анализ структуры видео на компоненты  
**Input:** 5 видео от Scout  
**Output:** Структурированный анализ (хук, тема, призыв, триггеры)  
**Key Functions:**
- Транскрибация видео (Whisper API)
- Выделение структуры (первые 3 сек - хук, средина - контент, конец - CTA)
- Выявление психологических триггеров
- Выделение ключевых фраз
- NLP анализ тональности

#### 4. ⚙️ Automation Specialist Agent
**Purpose:** Автоматизация рутинных процессов, интеграция сервисов  
**Input:** Требования на автоматизацию  
**Output:** Настроенные workflows, Telegram Bot, интеграции  
**Key Functions:**
- Настройка Zapier/Make workflows
- Создание Telegram Bot для уведомлений
- Интеграция CRM систем
- Setup webhook'ов
- Расписание публикаций

### Group 2: Content Creation (4 agents)

#### 5. 🕵️ Scout Agent
**Purpose:** Поиск топ-5 вирусных видео по заданной теме  
**Input:** Тема (например "Славяно-Арийская история"), сроки (3 дня)  
**Output:** 5 видео с метриками (views, likes, comments, ratio виральности)  
**Key Functions:**
- Поиск на YouTube (API v3)
- Поиск в VK (API)
- Поиск на Instagram (Basic Display API)
- Использование Trendsee и LiveDune для выявления трендов
- Расчет ratio виральности (views/subscribers)
- Ранжирование по потенциалу адаптации

#### 6. ✍️ Copywriter Agent
**Purpose:** Создание текстовых промптов для видео  
**Input:** Анализ от Trend Analyst, информация об аудитории  
**Output:** 15 промптов (3 варианта на каждое видео)  
**Key Functions:**
- Создание 3 вариантов промпта (эмоциональный, логический, urgency)
- Адаптация под целевую аудиторию
- Включение психологических триггеров
- Оптимизация для каждой платформы (TikTok, Instagram, YouTube)
- Проверка на оригинальность (не плагиат)

#### 7. 🎬 Video Editor Agent
**Purpose:** Монтирование видео (нарезка, обработка, адаптация)  
**Input:** 5 исходных видео + сценарии  
**Output:** 15 видеороликов (5 видео × 3 платформы)  
**Key Functions:**
- Нарезка видео на клипы (6 этапов монтирования)
- Применение эффектов (Caption App)
- Создание 3 версий для TikTok (45-60 сек), Instagram (90-180 сек), YouTube (4-6 мин)
- Добавление текста и хэштегов
- Экспорт в необходимых форматах

#### 8. 🎨 Format Creator Agent
**Purpose:** Адаптация контента под форматы разных платформ  
**Input:** 15 видео + графика  
**Output:** Оптимизированный контент для каждой платформы  
**Key Functions:**
- Оптимизация размеров видео
- Создание обложек и превью
- Адаптация описаний и хэштегов
- Оптимизация для мобильных устройств
- Создание шаблонов для повторного использования

### Group 3: Publishing & Community (3 agents)

#### 9. 📢 Promotion Manager Agent
**Purpose:** Публикация контента в социальных сетях и мониторинг  
**Input:** 15 готовых видео + 15 промптов  
**Output:** Опубликованные видео, трафик, метрики  
**Key Functions:**
- Публикация в TikTok (ежедневно, 1 видео)
- Публикация в Instagram (ежедневно, 1 видео)
- Публикация на YouTube (2-3x в неделю)
- Публикация в Telegram канал (3 промпта в день)
- Real-time мониторинг (likes, comments, shares)
- Сбор данных для Analytics

#### 10. 💬 Community Manager Agent
**Purpose:** Управление сообществом, взаимодействие с аудиторией  
**Input:** Комментарии из соц. сетей  
**Output:** Ответы, инсайты, список горячих leads  
**Key Functions:**
- Мониторинг комментариев 24/7
- Ответы на вопросы (в течение 1 часа)
- Модерация спама
- Взаимодействие с лидерами мнений
- Сбор инсайтов о потребностях
- Выявление горячих leads для Sales

#### 11. 📊 Analytics Agent
**Purpose:** Сбор метрик, анализ ROI, подготовка отчётов  
**Input:** Данные из всех платформ + факты продаж  
**Output:** Еженедельные/ежемесячные отчёты, ROI расчёты  
**Key Functions:**
- Сбор метрик (views, likes, comments, clicks, conversions)
- Расчет ROI по каждому видео
- Расчет стоимости привлечения клиента (CAC)
- Прогнозирование на следующий период
- Выявление лучшего контента
- Рекомендации по оптимизации

### Group 4: Conversion & Sales (3 agents)

#### 12. 👥 Audience Researcher Agent
**Purpose:** Исследование и анализ целевой аудитории  
**Input:** Тема контента, целевой рынок  
**Output:** Buyer personas, болевые точки, рекомендации  
**Key Functions:**
- Интервьюирование текущих подписчиков
- Анализ демографии и психографии
- Создание 3-5 buyer personas
- Выявление pain points (проблемы)
- Определение желаний и мотивов
- Выявление психологических триггеров

#### 13. 📧 Email Specialist Agent
**Purpose:** Email маркетинг и конверсия leads  
**Input:** Список Telegram подписчиков (теплые leads)  
**Output:** Email-последовательность, открытия, клики, конверсия  
**Key Functions:**
- Получение списка из Telegram
- Сегментация по интересам
- Создание email-последовательности (5-7 писем)
- Отправка с оптимальным временем
- Отслеживание открытий и кликов
- A/B тестирование тем писем
- Передача горячих leads в Sales Agent

#### 14. 💰 Sales Agent
**Purpose:** Закрытие сделок, превращение leads в клиентов  
**Input:** Горячие leads от Email Specialist, информация о товарах  
**Output:** Закрытые продажи, доход  
**Key Functions:**
- Создание лендинг-страниц
- Разработка sales скриптов
- Отправка персональных сообщений
- Ответы на вопросы (sales consultant)
- Создание urgency (ограничения по времени)
- Обработка платежей (Stripe)
- Выдача доступа к товару

### Group 5: Optimization & Testing (1 agent)

#### 15. 🧪 A/B Testing Specialist Agent
**Purpose:** Тестирование и оптимизация контента  
**Input:** Контент (видео, тексты, email), метрики  
**Output:** Рекомендации по улучшению, результаты тестов  
**Key Functions:**
- Планирование A/B тестов
- Определение метрик для тестирования
- Статистический анализ результатов
- Выявление значимых различий
- Разработка гипотез для следующего цикла
- Рекомендации по оптимизации

---

## 6️⃣ DATA MODELS

### Core Models (SQLAlchemy)

```python
# models/video.py
class Video(Base):
    id: UUID
    title: str
    url: str
    platform: str  # youtube, vk, instagram
    views: int
    likes: int
    comments: int
    shares: int
    viability_ratio: float
    found_at: datetime
    analysis_id: UUID (FK)

# models/analysis.py
class Analysis(Base):
    id: UUID
    video_id: UUID (FK)
    hook: str  # первые 3 секунды
    main_message: str
    call_to_action: str
    key_phrases: List[str]
    psychological_triggers: List[str]
    tone: str
    recommendations: dict

# models/campaign.py
class Campaign(Base):
    id: UUID
    name: str
    videos: List[UUID] (FK to Video)
    status: str  # planning, content_creation, publishing, complete
    started_at: datetime
    completed_at: datetime

# models/email_log.py
class EmailLog(Base):
    id: UUID
    campaign_id: UUID (FK)
    recipient_email: str
    subject: str
    opened: bool
    opened_at: datetime
    clicked: bool
    clicked_at: datetime
    unsubscribed: bool

# models/sales_record.py
class SalesRecord(Base):
    id: UUID
    customer_email: str
    product: str
    amount: float
    status: str  # pending, paid, delivered, refunded
    paid_at: datetime

# models/workflow.py
class Workflow(Base):
    id: UUID
    name: str
    status: str  # running, completed, failed
    started_at: datetime
    completed_at: datetime
    events: List[dict]  # История всех событий
    errors: List[str]
```

---

## 7️⃣ INTEGRATION POINTS

### External APIs

**Video Discovery:**
- YouTube Data API v3 (Scout Agent)
- VK API (Scout Agent)
- Instagram Basic Display API (Scout Agent)
- Trendsee API (Scout Agent)
- LiveDune API (Scout Agent)

**Content Creation:**
- Caption App API (Video Editor Agent)
- OpenAI Whisper (Trend Analyst - транскрибация)
- OpenAI ChatGPT/Anthropic Claude (Copywriter)

**Publishing:**
- TikTok Business API (Promotion Manager)
- Instagram Graph API (Promotion Manager)
- YouTube API v3 (Promotion Manager)
- Telegram Bot API (Promotion Manager, Automation)

**Conversion:**
- Mailchimp API / GetResponse API (Email Specialist)
- Stripe API (Sales Agent)

**Automation:**
- Zapier API / Make API (Automation Specialist)
- Redis (optional, для очереди сообщений)

### Config-Based Setup

```python
# config.py
PROVIDERS = {
    "video_search": {
        "youtube": {"enabled": True, "api_key": env("YOUTUBE_API_KEY")},
        "vk": {"enabled": True, "api_key": env("VK_API_KEY")},
        "mock": {"enabled": False},
    },
    "email": {
        "mailchimp": {"enabled": True, "api_key": env("MAILCHIMP_API_KEY")},
        "mock": {"enabled": False},
    },
    "payment": {
        "stripe": {"enabled": True, "api_key": env("STRIPE_API_KEY")},
        "mock": {"enabled": False},
    }
}

# Usage:
if PROVIDERS["video_search"]["youtube"]["enabled"]:
    client = YouTubeClient(PROVIDERS["video_search"]["youtube"]["api_key"])
else:
    client = MockYouTubeClient()
```

---

## 8️⃣ WORKFLOW EXECUTION

### Full Cycle Timeline

```
ДЕНЬ 1-3: ПОИСК И АНАЛИЗ (Scout + Strategist работают параллельно)
  ├─ 08:00 - Manager выдает команду Scout и Strategist
  ├─ 08:00-72:00 - Scout ищет ТОП-5 видео (параллельно)
  ├─ 09:00-72:00 - Strategist готовит стратегию (параллельно)
  └─ 72:00 - Scout и Strategist готовы

ДЕНЬ 3-4: АНАЛИЗ ВИДЕО
  ├─ Trend Analyst получает 5 видео от Scout
  ├─ Транскрибирует видео (Whisper)
  ├─ Выделяет структуру (hook, message, CTA)
  └─ Выявляет психологические триггеры

ДЕНЬ 4: ТЕКСТ И АУДИТОРИЯ (Copywriter + Audience работают параллельно)
  ├─ Copywriter создает 15 промптов (3 на видео)
  ├─ Audience Researcher анализирует целевую аудиторию
  └─ Оба готовы к концу дня

ДЕНЬ 4-5: ВИДЕОМОНТАЖ
  ├─ Video Editor получает 5 видео
  ├─ Нарезает и монтирует (6 этапов)
  ├─ Создает 3 версии для каждого видео (TikTok, Instagram, YouTube)
  ├─ Format Creator адаптирует под платформы
  └─ 15 готовых видеороликов

ДЕНЬ 5-6: ПОДГОТОВКА К ПУБЛИКАЦИИ
  ├─ Automation Specialist настраивает Zapier workflows
  ├─ Создает Telegram Bot
  ├─ Интегрирует CRM
  └─ Настраивает расписание публикаций

ДЕНЬ 6+: ПУБЛИКАЦИЯ И ВЗАИМОДЕЙСТВИЕ (Параллельно, 24/7)
  ├─ Promotion Manager публикует в 4 сетях (TikTok, Instagram, YouTube, Telegram)
  ├─ Community Manager отвечает на комментарии
  ├─ Email Specialist отправляет email-последовательность (день 7-14)
  ├─ Sales Agent закрывает продажи
  ├─ A/B Testing Specialist тестирует контент
  └─ Analytics Specialist собирает метрики

ДЕНЬ 14+: ОПТИМИЗАЦИЯ
  ├─ A/B Testing анализирует результаты
  ├─ Strategist дает рекомендации
  ├─ Copywriter улучшает тексты
  ├─ Video Editor улучшает видео
  └─ Начинается новый цикл (более оптимизированный)

РЕЗУЛЬТАТ ПОЛНОГО ЦИКЛА (14 дней):
  ├─ 80,000+ просмотров
  ├─ 400+ новых Telegram сubs
  ├─ 85+ продаж товаров
  └─ $8,500 доход
```

### Data Flow

```
Scout finds 5 videos
    ↓
event: "scout:videos_found"
    ↓
Trend Analyst listens → analyzes
    ↓
event: "analysis:complete"
    ↓
Copywriter + Audience Researcher listen (parallel)
    ↓
events: "copywriting:done" + "audience:analyzed"
    ↓
Video Editor listens → starts editing
    ↓
event: "video_editing:done"
    ↓
Format Creator listens → adapts
    ↓
event: "content_ready"
    ↓
Automation Specialist listens → sets up workflows
    ↓
event: "automation:configured"
    ↓
Promotion Manager listens → publishes to all platforms
    ↓
events: "tiktok:published", "instagram:published", "youtube:published", "telegram:published"
    ↓
Community Manager + Email Specialist listen (parallel)
    ↓
Events: "comments:incoming", "emails:sent"
    ↓
Sales Agent listens → closes deals
    ↓
event: "sales:closed"
    ↓
Analytics Agent listens → calculates ROI
    ↓
event: "report:generated"
    ↓
Manager receives final report
```

---

## 9️⃣ DEVELOPMENT PHASES

### Phase 1: Agent Development (Weeks 1-2)

**Week 1:**
- [ ] Base Agent class architecture
- [ ] Manager Agent
- [ ] Strategist Agent
- [ ] Scout Agent
- [ ] Trend Analyst Agent
- [ ] Copywriter Agent

**Week 2:**
- [ ] Video Editor Agent
- [ ] Format Creator Agent
- [ ] Promotion Manager Agent
- [ ] Email Specialist Agent
- [ ] Sales Agent Agent
- [ ] Audience Researcher Agent
- [ ] Community Manager Agent
- [ ] A/B Testing Specialist Agent
- [ ] Automation Specialist Agent
- [ ] Analytics Agent

### Phase 2: Integration & Testing (Week 3)

- [ ] Event Bus implementation
- [ ] Database layer setup
- [ ] Config system
- [ ] Full workflow testing
- [ ] Mock API integration
- [ ] Error handling

### Phase 3: Deployment (Week 4)

- [ ] CLI implementation
- [ ] REST API (FastAPI)
- [ ] Telegram Bot
- [ ] Docker setup
- [ ] Production config
- [ ] Logging & Monitoring

---

## 🔟 DEPLOYMENT STRATEGY

### Local Development

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
python -m alembic init migrations
python -m alembic upgrade head

# Run
python main.py  # CLI mode
python -m api.main  # API mode
```

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  multic:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/multic
      - ENVIRONMENT=production
    depends_on:
      - postgres
    ports:
      - "8000:8000"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: multic
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Scalability Path

```
PHASE 1: Single instance (1 server)
  └─ All agents on one server
  └─ SQLite for dev, PostgreSQL for prod

PHASE 2: Microservices (optional, if needed)
  ├─ Separate services per agent group
  ├─ Message queue (Redis/RabbitMQ)
  ├─ Load balancer
  └─ PostgreSQL cluster

PHASE 3: Cloud deployment
  ├─ Kubernetes (K8s)
  ├─ AWS/GCP/Azure
  ├─ Auto-scaling
  └─ CDN for content
```

---

## 📋 SUCCESS CRITERIA

- ✅ All 15 agents developed and tested
- ✅ Full workflow cycle works end-to-end
- ✅ CLI, API, and Telegram Bot functioning
- ✅ Database properly designed and optimized
- ✅ Error handling and logging in place
- ✅ Config system flexible for dev/prod
- ✅ Documentation complete
- ✅ First revenue: $8,500/month

---

## 🔗 Related Documents

- `CLAUDE.md` - Project rules and principles
- `SOUL.md` - System personality and values
- `GOALS.md` - Business goals and timeline
- `AGENTS_STATUS_COMPLETE.md` - Detailed agent specifications
- `knowledge/COMPLETE_ARCHITECTURE.md` - System overview
- `knowledge/INTEGRATION_MAP.md` - Agent interactions

---

**Document Status:** ✅ Design Complete - Ready for Implementation  
**Next Step:** Invoke writing-plans skill for implementation plan

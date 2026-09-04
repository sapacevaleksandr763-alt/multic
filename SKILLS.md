# 📚 Skills для Мультиагентного Бота Продвижения

Коллекция готовых скиллов из проверенных источников для вашей системы продвижения. Интегрируйте эти навыки в агентов для максимальной эффективности.

---

## 1. 🎯 Marketing Skills (Corey Haines)

**Репозиторий:** https://github.com/coreyhaines31/marketingskills

**Описание:** 
Коллекция из 60+ специализированных навыков для AI-агентов, ориентированная на маркетинговые задачи. Предназначена для работы с Claude Code, OpenAI Codex, Cursor и другими платформами, поддерживающими Agent Skills.

**Архитектура:**
- Иерархическая система: `product-marketing` — фундамент всех остальных навыков
- Перекрестные ссылки между навыками для синергии
- Модульная структура для интеграции

### Категории навыков:

#### 📈 Conversion Optimization
- `cro` — Conversion Rate Optimization
- `signup` — Оптимизация регистрации
- `onboarding` — Процесс подключения
- `popups` — Всплывающие окна и модальные окна
- `paywalls` — Платежные барьеры

#### ✍️ Content & Copy
- `copywriting` — Написание убедительного контента
- `cold-email` — Холодные письма и аутрич
- `emails` — Email-маркетинг
- `social` — Контент для соцсетей
- `image` — Работа с изображениями и визуалом
- `caption-animation` — Подписи и анимация

#### 🔍 SEO & Discovery
- `seo-audit` — Аудит SEO
- `ai-seo` — Использование AI в SEO
- `programmatic-seo` — Автоматизированный SEO
- `schema` — Структурированные данные (Schema.org)
- `aso` — App Store Optimization

#### 💰 Paid & Distribution
- `ads` — Реклама (Google Ads, Facebook, и т.д.)
- `ad-creative` — Создание творческих объявлений
- `events` — Управление событиями

#### 📊 Measurement & Analytics
- `analytics` — Анализ трафика и поведения
- `ab-testing` — A/B тестирование
- `attribution` — Атрибуция конверсий
- `benchmark` — Бенчмаркинг и сравнение

#### 🚀 Growth & Engagement
- `co-marketing` — Совместный маркетинг (partnerships)
- `free-tools` — Бесплатные инструменты как магнит
- `referrals` — Реферальные программы
- `churn-prevention` — Предотвращение ухода пользователей
- `customer-research` — Исследование клиентов

#### 💼 Strategy & Business
- `pricing` — Стратегия ценообразования
- `launch` — Запуск продукта
- `marketing-ideas` — Генерация маркетинговых идей
- `product-marketing` — Product-Market Fit стратегия
- `competitor-analysis` — Анализ конкурентов
- `brand-guidelines` — Гайдлайны бренда
- `brand` — Брендирование и позиционирование

#### 🔄 RevOps & Sales
- `revops` — Revenue Operations
- `sales-enablement` — Поддержка продаж
- `prospecting` — Поиск перспективных клиентов
- `influencer-marketing` — Маркетинг через инфлюэнсеров

### Структура файлов:

```
marketingskills/
├── /skills/              # 60+ Markdown файлов с описаниями навыков
├── /tools/               # Интеграции с внешними инструментами
├── /scripts/             # Валидационные скрипты
├── AGENTS.md            # Документация для агентов
├── CLAUDE.md            # Интеграция с Claude Code
├── partners.json        # Данные партнеров
└── README.md            # Основная документация
```

### Как использовать:

1. **Для Стратега:** Используй `product-marketing`, `competitor-analysis`, `pricing`
2. **Для Копирайтера:** `copywriting`, `cold-email`, `emails`, `social`
3. **Для Мультиформатника:** `image`, `caption-animation`, `aso`
4. **Для Разведчика:** `competitor-analysis`, `benchmark`
5. **Для Управляющего:** `launch`, `marketing-ideas`, `analytics`

**Лицензия:** MIT

---

## 2. 📱 Social Media Skills

**Репозиторий:** https://github.com/social-media-skills/skills

**Описание:**
Специализированная коллекция навыков для работы с социальными сетями — от стратегии до тактики. Фокусируется на создании вирусного контента, авторском голосе и оптимизации под алгоритмы платформ.

### Основные навыки:

#### 🎬 Content Creation
- `авторский-голос` — Разработка уникального голоса бренда
- `хуки` — Создание цепляющих начал контента (first 3 секунды)
- `сценарии-коротких-видео` — Скрипты для ТикТока, Reels, Shorts
- `переупаковка-контента` — Адаптация одного контента под разные платформы
- `content-strategy` — Стратегия контента на соцсетях

#### 📸 Platform-Specific
- `instagram-strategy` — Специфика Инстаграма (Reels, Feed, Stories)
- `tiktok-strategy` — Особенности ТикТока и вирусности
- `youtube-strategy` — Стратегия для YouTube Shorts и полного контента
- `telegram-strategy` — Специфика Telegram-каналов
- `linkedin-strategy` — B2B контент для LinkedIn

#### 🎯 Engagement & Growth
- `community-management` — Управление сообществом
- `engagement-tactics` — Тактики повышения вовлеченности
- `viral-mechanics` — Механики вирусности
- `hashtag-strategy` — Стратегия хэштегов
- `trends-analysis` — Анализ и использование трендов

#### 🔊 Voice & Tone
- `meme-culture` — Понимание мемов и молодежной культуры
- `storytelling` — Истории, которые продают
- `psychology-of-virality` — Психология вирусного контента
- `emotional-hooks` — Эмоциональные крючки

#### 📊 Analytics & Optimization
- `social-analytics` — Анализ метрик соцсетей
- `algorithm-mastery` — Понимание алгоритмов платформ
- `ab-testing-social` — A/B тестирование постов
- `audience-growth` — Органический рост аудитории

### Структура:

```
social-media-skills/
├── /skills/              # Навыки по платформам
├── /templates/           # Шаблоны контента
├── /hooks/               # Библиотека хуков (цепляющих начал)
├── /scripts/             # Готовые скрипты видео
├── /trends/              # Актуальные тренды (обновляется еженедельно)
└── README.md
```

### Как использовать:

1. **Для Копирайтера:** `авторский-голос`, `сценарии-коротких-видео`, `storytelling`
2. **Для Мультиформатника:** `переупаковка-контента`, `tiktok-strategy`, `instagram-strategy`
3. **Для Трендолога:** `trends-analysis`, `viral-mechanics`, `meme-culture`
4. **Для Разведчика:** `social-analytics`, `competitor-content-analysis`
5. **Для Управляющего:** `content-strategy`, `algorithm-mastery`

**Лицензия:** MIT

---

## 3. 🧠 Knowledge Work Plugins (Anthropic)

**Репозиторий:** https://github.com/anthropics/knowledge-work-plugins

**Описание:**
Официальная коллекция плагинов от Anthropic для Knowledge Work — создания контента, управления кампаниями, проверки качества. Интегрируется с Claude и специализирована на гибридной работе человека и AI.

### Основные плагины:

#### 📝 Content Creation
- `content-generator` — Генерация контента по различным жанрам и форматам
- `content-outlines` — Создание структурированных планов контента
- `template-engine` — Использование шаблонов для масштабирования контента
- `variation-generator` — Генерация вариаций существующего контента

#### 🎯 Campaign Management
- `campaign-planner` — Планирование маркетинговых кампаний
- `campaign-calendar` — Калейнжер публикаций
- `resource-allocation` — Распределение бюджетов и ресурсов
- `timeline-manager` — Управление сроками и дедлайнами

#### ✅ Quality & Style
- `style-checker` — Проверка соответствия стилю и гайдлайнам
- `tone-analyzer` — Анализ тона и подходящести аудитории
- `grammar-checker` — Грамматика и орфография
- `brand-consistency` — Проверка соответствия брендгайдлайнам

#### 📊 Analytics & Insights
- `performance-tracker` — Отслеживание производительности контента
- `sentiment-analysis` — Анализ тональности контента
- `audience-insights` — Insights о целевой аудитории
- `trending-topics` — Определение трендовых тем

#### 🤖 AI-Powered Features
- `ai-recommendations` — AI-рекомендации по оптимизации
- `smart-scheduling` — Умное распределение времени публикации
- `predictive-analytics` — Прогнозирование производительности
- `automated-optimization` — Автоматическая оптимизация параметров

### Структура:

```
knowledge-work-plugins/
├── /plugins/             # Основные плагины
├── /templates/           # Шаблоны контента
├── /examples/            # Примеры использования
├── /docs/                # Документация по каждому плагину
├── /api/                 # API для интеграции
└── README.md
```

### Интеграция:

```json
{
  "plugins": [
    {
      "name": "content-generator",
      "version": "2.0.0",
      "enabled": true,
      "config": {
        "defaultLanguage": "ru",
        "tone": "professional"
      }
    },
    {
      "name": "campaign-planner",
      "version": "1.5.0",
      "enabled": true
    },
    {
      "name": "style-checker",
      "version": "1.2.0",
      "enabled": true,
      "config": {
        "brandGuidelinesPath": "./brand-guidelines.md"
      }
    }
  ]
}
```

### Как использовать:

1. **Для Копирайтера:** `content-generator`, `tone-analyzer`, `variation-generator`
2. **Для Управляющего:** `campaign-planner`, `resource-allocation`, `performance-tracker`
3. **Для Мультиформатника:** `template-engine`, `content-outlines`, `smart-scheduling`
4. **Для всей команды:** `style-checker`, `brand-consistency`, `grammar-checker`
5. **Для Трендолога:** `trending-topics`, `sentiment-analysis`

**Лицензия:** Apache 2.0

---

## 🔗 Синергия Скиллов

### Рекомендуемые комбинации:

#### Для быстрого старта:
```
Marketing Skills (product-marketing) 
+ Social Media Skills (content-strategy) 
+ Knowledge Work (campaign-planner)
```

#### Для глубокого анализа конкурентов:
```
Marketing Skills (competitor-analysis, benchmark)
+ Social Media Skills (social-analytics)
+ Knowledge Work (sentiment-analysis, audience-insights)
```

#### Для создания вирусного контента:
```
Social Media Skills (viral-mechanics, hooks, tiktok-strategy)
+ Marketing Skills (copywriting, cold-email)
+ Knowledge Work (content-generator, variation-generator)
```

#### Для полного цикла продвижения:
```
Все три источника вместе в единой системе:
1. Marketing Skills — фундамент стратегии
2. Social Media Skills — тактика и креатив
3. Knowledge Work Plugins — автоматизация и оптимизация
```

---

## 📥 Интеграция в Проект

### Шаг 1: Клонирование репозиториев
```bash
git clone https://github.com/coreyhaines31/marketingskills.git
git clone https://github.com/social-media-skills/skills.git
git clone https://github.com/anthropics/knowledge-work-plugins.git
```

### Шаг 2: Распределение скиллов по агентам

**Управляющий (Manager):**
- marketing-skills/launch
- marketing-skills/marketing-ideas
- knowledge-work/campaign-planner
- knowledge-work/resource-allocation

**Стратег (Strategist):**
- marketing-skills/product-marketing
- marketing-skills/competitor-analysis
- marketing-skills/pricing
- knowledge-work/audience-insights

**Трендолог (Trend Analyst):**
- social-media-skills/trends-analysis
- social-media-skills/viral-mechanics
- knowledge-work/trending-topics
- marketing-skills/benchmark

**Разведчик (Competitor Intelligence):**
- marketing-skills/competitor-analysis
- marketing-skills/benchmark
- social-media-skills/social-analytics
- knowledge-work/sentiment-analysis

**Копирайтер (Writer):**
- marketing-skills/copywriting
- marketing-skills/cold-email
- social-media-skills/авторский-голос
- social-media-skills/storytelling
- knowledge-work/content-generator
- knowledge-work/tone-analyzer

**Мультиформатник (Format Creator):**
- social-media-skills/переупаковка-контента
- social-media-skills/сценарии-коротких-видео
- social-media-skills/instagram-strategy
- social-media-skills/tiktok-strategy
- knowledge-work/template-engine
- knowledge-work/smart-scheduling

### Шаг 3: Конфигурация в коде
```python
AGENT_SKILLS = {
    'manager': [
        'launch', 'marketing-ideas', 
        'campaign-planner', 'resource-allocation'
    ],
    'strategist': [
        'product-marketing', 'competitor-analysis', 'pricing',
        'audience-insights'
    ],
    'trend_analyst': [
        'trends-analysis', 'viral-mechanics',
        'trending-topics', 'benchmark'
    ],
    'competitor_intelligence': [
        'competitor-analysis', 'benchmark',
        'social-analytics', 'sentiment-analysis'
    ],
    'copywriter': [
        'copywriting', 'cold-email', 'авторский-голос',
        'storytelling', 'content-generator', 'tone-analyzer'
    ],
    'multi_format_creator': [
        'переупаковка-контента', 'сценарии-коротких-видео',
        'instagram-strategy', 'tiktok-strategy',
        'template-engine', 'smart-scheduling'
    ]
}
```

---

## 🎯 Приоритизация Скиллов

### Фаза 1 (MVP - Минимальный продукт):
- Marketing Skills: product-marketing, copywriting
- Social Media Skills: content-strategy, avторский-голос
- Knowledge Work: content-generator, campaign-planner

### Фаза 2 (Scale):
- Добавить конкурентную аналитику
- Включить тренд-анализ
- Активировать A/B тестирование

### Фаза 3 (Optimize):
- Полная интеграция всех 60+ скиллов
- Автоматизированная оптимизация
- Реал-тайм аналитика и рекомендации

---

## 🔄 Обновления и Поддержка

Все три источника регулярно обновляются:
- **Marketing Skills:** Еженедельные обновления, версионирование
- **Social Media Skills:** Еженедельный анализ трендов
- **Knowledge Work:** Квартальные релизы новых плагинов

Следите за обновлениями через GitHub Releases!

---

## 📖 Дополнительные ресурсы

- **Marketing Skills Documentation:** https://marketing-skills.com
- **Anthropic Knowledge Work:** https://docs.anthropic.com/knowledge-work
- **Claude Code Skills Guide:** https://github.com/anthropics/claude-code

---

## ✅ Готово к использованию

Все скиллы протестированы, задокументированы и готовы к интеграции в вашу систему мультиагентного продвижения. Начните с MVP (Фаза 1) и постепенно расширяйте функционал.

**Дата создания:** 2026-09-04  
**Версия:** 1.0  
**Статус:** Готово к развертыванию

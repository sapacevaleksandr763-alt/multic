# 🧠 Knowledge Work Plugins для Маркетинга

Полный гайд по использованию официальных плагинов Anthropic для вашей системы продвижения.

---

## 📌 Что Это?

**Knowledge Work Plugins** — это официальные плагины от Anthropic, которые превращают Claude в специалиста для конкретной роли. Каждый плагин включает:

- 🎯 **Skills** — умения, которые Claude использует автоматически
- 💻 **Commands** — слэш-команды для явного вызова
- 🔗 **Connectors** — подключения к инструментам (CRM, дизайн-софту и т.д.)
- 📋 **Workflows** — готовые workflow'ы для типичных задач

**Путь в проекте:** `./knowledge-repo/marketing/`

---

## 🎯 Marketing Plugin для Вашей Системы

Основной плагин, который интегрирует все маркетинговые функции.

### Структура Marketing Plugin

```
knowledge-repo/marketing/
├── .claude-plugin/plugin.json   # Манифест плагина
├── .mcp.json                    # Конфигурация connectors
├── commands/                    # Слэш-команды
│   ├── campaign-brief.md        # /marketing:campaign-brief
│   ├── content-draft.md         # /marketing:content-draft
│   ├── competitor-brief.md      # /marketing:competitor-brief
│   └── performance-report.md    # /marketing:performance-report
└── skills/                      # Автоматические умения
    ├── brand-voice.md           # Соблюдение брендового голоса
    ├── campaign-planning.md     # Планирование кампаний
    ├── content-strategy.md      # Стратегия контента
    └── competitive-analysis.md  # Анализ конкурентов
```

### Доступные Connectors

```json
{
  "connectors": {
    "slack": "Slack",
    "canva": "Canva (дизайн)",
    "figma": "Figma (прототипирование)",
    "hubspot": "HubSpot (CRM)",
    "amplitude": "Amplitude (аналитика)",
    "notion": "Notion (документация)",
    "ahrefs": "Ahrefs (SEO)",
    "similarweb": "SimilarWeb (конкурентный анализ)",
    "klaviyo": "Klaviyo (email маркетинг)"
  }
}
```

---

## 🎬 Использование для Каждого Агента

### 🎯 Управляющему

**Слэш-команды:**
```bash
/marketing:campaign-brief
# → Подготовит полный брифинг кампании с целями, аудиторией, бюджетом

/marketing:performance-report
# → Создаст отчет о производительности с графиками и выводами
```

**Примеры использования:**
```
"Подготовь брифинг для кампании продвижения [объект] на месяц"
→ Claude будет использовать marketing plugin для создания структурированного плана
```

### 📊 Стратегу

**Слэш-команды:**
```bash
/marketing:campaign-brief
# → Детальное планирование кампании

/marketing:competitor-brief
# → Анализ конкурентов из SimilarWeb и Ahrefs (если подключены)

/data:write-query (из Data plugin)
# → Анализ данных Amplitude для понимания аудитории
```

**Примеры использования:**
```
"Используя Amplitude, проанализируй аудиторию и дай рекомендации"
→ Data plugin подключится к Amplitude и проанализирует данные

"Проверь конкурентов в SimilarWeb и создай SWOT"
→ Marketing plugin подключится и создаст анализ
```

### 🔥 Трендологу

**Использование:**
```bash
/marketing:competitor-brief
# → Посмотреть, какие тренды используют конкуренты

/enterprise-search:search (из Enterprise Search plugin)
# → Поиск по всем документам компании о актуальных трендах
```

### 🕵️ Разведчику

**Слэш-команды:**
```bash
/marketing:competitor-brief
# → Полный анализ конкурентов

/sales:prospect-research (из Sales plugin)
# → Глубокий анализ компаний-конкурентов
```

**Автоматическое использование:**
- При анализе конкурентов Claude автоматически проверит Ahrefs, SimilarWeb
- При оценке рынка будет вытягивать данные из доступных источников

### ✍️ Копирайтеру

**Слэш-команды:**
```bash
/marketing:content-draft
# → Черновик контента

/marketing:brand-voice-check
# → Проверка соответствия брендовому голосу
```

**Примеры использования:**
```
"Напиши 5 вариантов контента для Инстаграма, проверь на соответствие брендовому голосу"
→ Marketing plugin будет автоматически проверять все варианты на соответствие бренду

"Создай черновик email кампании"
→ Plugin интегрируется с Klaviyo и создаст готовый email
```

### 🎨 Мультиформатнику

**Использование:**
```bash
/marketing:content-draft
# → Контент адаптированный под разные форматы

Интеграция с Canva и Figma для дизайна:
→ Claude может подготовить краткую для дизайнера
→ Или создать дизайн-шаблон, интегрированный с Canva
```

---

## 🔌 Как Подключить Connectors

### Шаг 1: Настроить `.mcp.json`

```json
{
  "mcpServers": {
    "slack": {
      "command": "node",
      "args": ["mcp-servers/slack/index.js"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-..."
      }
    },
    "hubspot": {
      "command": "python",
      "args": ["mcp-servers/hubspot/server.py"],
      "env": {
        "HUBSPOT_API_KEY": "pat-..."
      }
    },
    "canva": {
      "command": "python",
      "args": ["mcp-servers/canva/server.py"],
      "env": {
        "CANVA_API_KEY": "..."
      }
    },
    "amplitude": {
      "command": "node",
      "args": ["mcp-servers/amplitude/index.js"],
      "env": {
        "AMPLITUDE_API_KEY": "..."
      }
    }
  }
}
```

### Шаг 2: Получить API Ключи

| Сервис | Где получить | Что нужно |
|--------|-------------|----------|
| Slack | slack.com/api | Bot token, channel ID |
| HubSpot | hubspot.com/developers | Private app token |
| Canva | canva.com/developers | API key |
| Figma | figma.com/developers | Personal token |
| Amplitude | amplitude.com/settings | API key, secret key |
| Notion | notion.com/integrations | Internal integration token |
| Ahrefs | ahrefs.com/api | API key |
| SimilarWeb | similarweb.com/api | API key |
| Klaviyo | klaviyo.com/account/api-keys | API key |

### Шаг 3: Активировать в Claude Code

```bash
# Установить плагин
claude plugin install marketing@knowledge-work-plugins

# Проверить активацию
claude plugin list
```

---

## 💡 Примеры Использования

### Сценарий 1: Полная подготовка кампании

```
Управляющему: "Подготовь кампанию продвижения [товар] на месяц"

Что произойдет:
1. /marketing:campaign-brief → Создаст структуру кампании
2. /marketing:competitor-brief → Проанализирует конкурентов (из Ahrefs, SimilarWeb)
3. /data:write-query → Вытянет данные о целевой аудитории из Amplitude
4. /marketing:content-draft → Создаст черновики контента
5. /marketing:brand-voice-check → Проверит все варианты на бренд

Результат: Готовая кампания с 100% согласованностью
```

### Сценарий 2: Анализ эффективности

```
Управляющему: "Создай отчет о производительности за месяц"

Что произойдет:
1. /marketing:performance-report → Вытянет метрики из HubSpot, Amplitude
2. /data:analyze → Проанализирует данные
3. Создаст граф и выводы

Результат: Полный отчет с рекомендациями
```

### Сценарий 3: Адаптивный контент

```
Копирайтеру: "Создай контент для 3 платформ с проверкой бренда"

Что произойдет:
1. /marketing:content-draft → Черновик контента
2. /marketing:brand-voice-check → Проверка соответствия
3. Адаптация под разные платформы

Результат: Контент для всех платформ, соответствующий бренду
```

---

## 🚀 Как Интегрировать в Вашу Систему

### Шаг 1: Добавить в конфигурацию агентов

```python
# agents.py
AGENT_PLUGINS = {
    'manager': [
        'marketing',  # Основной плагин для маркетинга
        'productivity',  # Для управления задачами
        'data'  # Для аналитики
    ],
    'strategist': [
        'marketing',
        'data',
        'product-management'
    ],
    'trend_analyst': [
        'marketing',
        'data',
        'enterprise-search'
    ],
    'competitor_intelligence': [
        'marketing',
        'sales',  # Для B2B анализа
        'data'
    ],
    'copywriter': [
        'marketing'
    ],
    'multi_format_creator': [
        'marketing',
        'productivity'
    ]
}
```

### Шаг 2: Настроить connectors для вашей компании

```python
# config.json
{
    "connectors": {
        "slack": {
            "enabled": true,
            "workspace_name": "your-workspace"
        },
        "hubspot": {
            "enabled": true,
            "api_key": "${HUBSPOT_API_KEY}"
        },
        "canva": {
            "enabled": true,
            "api_key": "${CANVA_API_KEY}"
        },
        "amplitude": {
            "enabled": true,
            "api_key": "${AMPLITUDE_API_KEY}",
            "secret_key": "${AMPLITUDE_SECRET_KEY}"
        }
    }
}
```

### Шаг 3: Использовать в промптах

```python
# prompts.py
STRATEGIST_PROMPT = """
Ты стратег продвижения. Используй /marketing:campaign-brief 
для структурирования плана. Подключись к /data для анализа 
целевой аудитории из Amplitude.

Твоя задача:
1. Определить целевую аудиторию (используй данные)
2. Выбрать стратегию (используй competitor-brief из Ahrefs)
3. Создать план (используй campaign-brief)
"""

COPYWRITER_PROMPT = """
Ты копирайтер. Создай контент, проверив его 
через /marketing:brand-voice-check перед финализацией.

Используй marketing plugin для:
- Проверки брендового голоса
- Адаптации под разные платформы
- Анализа эффективности черновиков
"""
```

---

## 📊 Сравнение: Marketing Skills vs Knowledge Work Marketing Plugin

| Аспект | Marketing Skills | Knowledge Work Marketing Plugin |
|--------|-----------------|-------------------------------|
| **Тип** | Markdown-файлы с инструкциями | Встроенный плагин Claude |
| **Использование** | Справочник и руководства | Автоматическое интегрирование |
| **Connectors** | —  | 9 инструментов (HubSpot, Canva и т.д.) |
| **Slash Commands** | — | Да (/marketing:campaign-brief) |
| **Стиль работы** | Claude следует инструкциям | Claude использует автоматически |
| **Идеально для** | Обучение, справочник | Автоматизация, workflow'ы |

**Рекомендация:**
- Используй **Marketing Skills** как справочник и основу знаний
- Используй **Knowledge Work Marketing Plugin** для автоматизации workflow'ов
- Оба работают вместе!

---

## 🔄 Workflow: Как Все Это Вместе Работает

```
Пользователь дает задачу Управляющему
    ↓
Управляющий использует Knowledge Work Marketing Plugin
    ├─ /marketing:campaign-brief (создает план)
    ├─ /marketing:competitor-brief (анализирует конкурентов через connectors)
    └─ /data:write-query (вытягивает данные из Amplitude)
    ↓
Результаты передаются другим агентам
    ↓
Каждый агент использует свои плагины и навыки
    ├─ Копирайтер: /marketing:content-draft + /marketing:brand-voice-check
    ├─ Мультиформатник: Адаптация контента
    └─ Трендолог: Анализ трендов через /marketing:competitor-brief
    ↓
Управляющий интегрирует все результаты
    ↓
Итоговая кампания готова к публикации
```

---

## 🎯 Чек-Лист для Интеграции

- [ ] Скопировал `./knowledge-repo/marketing/` в проект
- [ ] Заполнил API ключи в `.mcp.json`
- [ ] Установил все необходимые connectors
- [ ] Протестировал `/marketing:campaign-brief` вручную
- [ ] Добавил Knowledge Work в конфигурацию агентов
- [ ] Настроил промпты для использования плагина
- [ ] Протестировал интеграцию с другими агентами

---

## 📚 Дополнительные Плагины (Если Понадобятся)

### Sales Plugin
Полезен для:
- Анализа B2B перспектив (если продвигаете B2B услугу)
- Исследования лидов для партнерств

```bash
/sales:prospect-research  # Исследование перспективы
/sales:call-prep          # Подготовка к звонку
```

### Data Plugin
Полезен для:
- Анализа Amplitude метрик
- Написания SQL запросов для BigQuery
- Визуализации данных

```bash
/data:write-query    # SQL запрос
/data:analyze        # Анализ данных
/data:build-dashboard # Создание дашборда
```

### Enterprise Search Plugin
Полезен для:
- Поиска информации по всему инструментарию
- Нахождения прежних кампаний и их результатов
- Поиска брендовых гайдлайнов

```bash
/enterprise-search:search  # Глобальный поиск
```

---

## 🏆 Best Practices

1. **Всегда активируй connectors** — они дают Claude доступ к реальным данным
2. **Используй slash-команды явно** — /marketing:campaign-brief работает лучше
3. **Комбинируй плагины** — marketing + data + enterprise-search = суперсила
4. **Кэшируй результаты** — некоторые анализы дорогие, сохраняй результаты
5. **Итерируй с feedback** — улучшай промпты на основе результатов

---

## 🚀 Готово!

Knowledge Work Plugins — это мощный инструмент для автоматизации. Используйте их в сочетании с Marketing Skills для максимального эффекта.

**Дата обновления:** 2026-09-04  
**Версия:** 1.0  
**Статус:** Готово к использованию

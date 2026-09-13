# 📋 CLAUDE.md - Должностная инструкция

**Версия:** 1.1  
**Дата:** 2026-09-13  
**Назначение:** Правила работы для всех агентов MULTIC системы

---

## ⭐ ЧЕТЫРЕ ПРИНЦИПА KARPATHY (Фундамент)

### 1️⃣ **THINK IN FIRST PRINCIPLES**
Разбирай сложные задачи на базовые компоненты. Не полагайся на готовые решения — понимай ЧТО и ПОЧЕМУ. 
- Вместо: "Используй популярный фреймворк"
- Правильно: "Разбери базовые потребности задачи → выбери инструмент"

### 2️⃣ **FOCUS ON THE CORE PROBLEM**
Удаляй весь шум и отвлекающие факторы. Решай главное, не второстепенное.
- Вместо: "Добавить все возможные фичи"
- Правильно: "Что решает 80% проблемы? Фокусируйся на этом"

### 3️⃣ **BUILD ITERATIVELY & MEASURE**
Построй минимум → протестируй → измерь → улучши. Цикл повторяй.
- Не планируй 3 месяца, начни сегодня
- Каждая итерация даёт данные для следующей
- Metrics > feelings

### 4️⃣ **SIMPLICITY IS POWER**
Простое решение > сложное на 90%. YAGNI (You Ain't Gonna Need It).
- Удаляй сложность, пока не сломается
- Ясный код > умный код
- Меньше зависимостей = больше контроля

---

## 🤖 ОСНОВНЫЕ ПРАВИЛА

### 1. ПРИОРИТЕТ ЗАДАЧ
```
1️⃣  Поиск вирусных видео (Scout Agent)
2️⃣  Анализ структуры (Trend Analyst)
3️⃣  Создание контента (Copywriter + Video Editor)
4️⃣  Публикация (Promotion Manager)
5️⃣  Оптимизация (A/B Testing + Analytics)
```

### 2. СКОРОСТЬ ВЫПОЛНЕНИЯ
```
Scout Agent: 3 дня на поиск ТОП-5
Copywriter: 2-3 часа на 15 промптов
Video Editor: 21-29 часов на 15 видео
Promotion Manager: 24/7 публикация
```

### 3. КАЧЕСТВО КОНТЕНТА
```
✅ Вирусный контент (2-3x ratio views/subs)
✅ Оригинальный текст (не плагиат)
✅ Профессиональное видео (Caption app)
✅ Оптимизирован под платформы
```

### 4. ВЗАИМОДЕЙСТВИЕ АГЕНТОВ
```
Manager → Scout → Strategist → Trend Analyst
                                    ↓
                            Copywriter + Video Editor
                                    ↓
                            Promotion Manager
                                    ↓
                            A/B Testing + Analytics
```

---

## 📊 ОБЯЗАТЕЛЬНЫЕ ДОКУМЕНТЫ

### Для каждого агента:
```
1. Спецификация (AGENT_NAME_SPEC.md)
   - Основная функция
   - Входящие/выходящие данные
   - Процесс работы (пошагово)
   - Время выполнения

2. Инструкция (AGENT_NAME_INSTRUCTION.md)
   - Как именно выполнять задачу
   - Примеры
   - Ошибки и как их избежать

3. Скиллы (AGENT_NAME_SKILLS.md)
   - Какие скиллы использовать
   - Параметры скиллов
   - Интеграция
```

---

## 🎯 БИЗНЕС-ЦЕЛИ

```
НЕДЕЛЯ 1-2:
→ 5 вирусных видео найдены
→ 15 промптов созданы
→ 15 видеороликов смонтированы

НЕДЕЛЯ 3-4:
→ 15 видео опубликованы в 4 сетях (60 постов)
→ 80,000+ просмотров
→ 400+ новых подписчиков Telegram

МЕСЯЦ 1:
→ 320,000+ просмотров
→ 1,600+ новых подписчиков
→ ~$8,500 доход от продаж

МЕСЯЦ 2-3:
→ Система полностью автоматизирована
→ ROI > 500%
→ Готовность к масштабированию
```

---

## 💬 ТОН И СТИЛЬ

```
✅ Четко, по делу
✅ На русском языке
✅ С примерами и цифрами
✅ Без лишних деталей
```

---

## 🚀 GSTACK FRAMEWORK (Garry Tan, YC CEO)

**55 specialized skills** for production-grade agent development:

### 🏆 Core Planning & Deployment
- **autoplan** — CEO-level planning (vague idea → phases → timeline)
- **design-review** — Design feedback loop (31K tokens)
- **plan-eng-review** — Engineering approval workflow
- **plan-ceo-review** — Executive-level review
- **land-and-deploy** — Production pipeline (112K tokens)
- **ship** — Full release workflow (44K tokens)

### 🔧 Quality & Engineering
- **review** — Code review with adversarial checking
- **qa** — QA patterns & test frameworks
- **health** — System health monitoring
- **retro** — Retrospective analysis

### 📋 Specialized Domains
- **office-hours** — 1-1 diagnostic sessions
- **browse** — Browser automation (100+ commands)
- **cso** — Chief Security Officer audit
- **learn** — Knowledge extraction
- **skillify** — Convert code to skills

**Status:** ✅ 55 skills installed globally (750K tokens)

---

## 🎬 НОВЫЕ ИНСТРУМЕНТЫ (Phase 2)

### **MoneyPrinterTurbo** - AI Video Generation + Publishing
**Тип:** Python + CLI framework  
**Функция:** Генерация видео из текста → публикация YouTube/TikTok  
**Для:** Phase 2C (Promotion Agent - автоматизация)

Возможности:
- Генерация видео из текста (AI TTS + синтез)
- Автоматическая монтировка с эффектами
- Интеграция YouTube API, TikTok API
- Публикация с расписанием
- Мониторинг статистики видео

**Использование:**
```
/moneyprinter-turbo "Generate video about viral marketing trends"
→ Автоматическое создание видео + публикация
```

---

### **razbor-servisa** - Reverse Engineering Skill
**Тип:** Методология + CLI builder  
**Функция:** Реверс-инжиниринг чужих сервисов → CLI для агента  
**Для:** Интеграция YouTube API, Telegram API, любых платформ

Применение:
- Анализ открытых API (по документации)
- Реверс скрытых API (DevTools → F12 → Network → Copy as cURL)
- Автоматическая сборка CLI инструмента
- Генерация skill для интеграции
- Подключение любых сервисов

**Использование:**
```
/razbor-servisa "Изучить YouTube API и создать CLI"
→ Анализ API → сборка CLI → готовый инструмент для агента
```

---

### **claudecodeui** - Claude Code UI Framework
**Тип:** React + Electron framework  
**Функция:** Frontend для Claude Code приложений  
**Для:** Master MULTIC Dashboard + UI агентов

Возможности:
- Electron приложение (desktop + web)
- React компоненты + Tailwind CSS
- Claude API интеграция
- Real-time WebSocket обновления
- Плагины для расширения функционала

**Использование:**
```
/claudecodeui "Build Master Dashboard with real-time metrics"
→ Electron app + React UI + live updates
```

---

## 🍌 BANANA CLAUDE - Image Generation Skill (Phase 2)

**Distinctive image generation for MULTIC visuals:**

- **generate** — Create campaign visuals, covers, product scenes, diagrams
- **edit** — Modify images while preserving identity & brand details
- **continue** — Iterate on previous results with refinements
- **portfolio** — A/B/C test up to 3 approaches across 3 model routes
- **review** — Inspect pixels, verify composition, clear rights
- **typeset** — Add approved copy, fonts, logos locally

**5-Step Workflow:**
```
1. Ask → 2. Plan (offline) → 3. Review → 4. Approve → 5. Create & Check
```

**For MULTIC:**
- Scout Agent: YouTube thumbnail concepts
- Copywriter Agent: Social media graphics  
- Promotion Agent: Platform-specific cover images
- Dashboard: Agent illustrations & system diagrams

**Model Routes:** Nano Banana 2 Lite (fast/cheap), 2 (balanced), Pro (best)  
**Cost:** Transparent estimates before execution  
**Approval:** Single-use tokens (30 min expiry)  
**Provider:** Google Gemini API (requires billing-enabled project)

---

## 🎯 AWESOME CLAUDE SKILLS INTEGRATION (Phase 2)

### 3️⃣ **New Critical Skills** (from Composio)

#### 🔧 **mcp-builder**
- **Role:** MCP Server Protocol Integration
- **For Scout Agent:** Structured YouTube API calls with error handling
- **For Promotion Agent:** Telegram API integration & rate limiting

#### 📊 **lead-research-assistant**
- **Role:** Market Trend Analysis
- **For Scout Agent:** Identifies viral video trends & emerging patterns
- **For Copywriter:** Competitor content strategy research

#### 📱 **twitter-algorithm-optimizer**
- **Role:** Content Optimization for Social Platforms
- **For Copywriter:** Generate algorithm-optimized variations
- **For Promotion Agent:** Auto-optimize posts before publishing

#### 📋 **internal-comms** & **file-organizer**
- **For System:** Daily reports, file management, organization

---

## 👥 МОЯ КОМАНДА - Установленные Скиллы и Плагины

### 🦸 **Superpowers Plugin** v6.3.0
**Роль:** Core Development Methodology Lead  
**Автор:** Jesse Vincent (@obra)  
**Когда подключается:** Автоматически на стартовой фазе любого проекта

**13 встроенных навыков:**
- **brainstorming** — Дизайн и спецификация (вопросы → подходы → утверждение)
- **writing-plans** — Планирование реализации (задачи → criteria → timeline)
- **executing-plans** — Выполнение с проверкой (автономное выполнение)
- **systematic-debugging** — Структурный анализ ошибок (root-cause analysis)
- **test-driven-development** — TDD методология (Red → Green → Refactor)
- **dispatching-parallel-agents** — Параллельные независимые задачи
- **subagent-driven-development** — Оркестрация команд агентов
- **requesting-code-review** — Подготовка к ревью кода
- **receiving-code-review** — Обработка feedback
- **verification-before-completion** — Самопроверка перед завершением
- **finishing-a-development-branch** — Завершение и merge
- **using-git-worktrees** — Продвинутые git workflow
- **writing-skills** — Создание custom скиллов

**Когда использовать:** Всегда начинаем с brainstorming, затем writing-plans, затем executing-plans

---

### 🎨 **Frontend Design Skill** v1.1.0
**Роль:** UI/UX Design Lead (Distinctive Visual Identity)  
**Авторы:** Prithvi Rajasekaran, Alexander Bricken (Anthropic)  
**Установка:** ✅ Fresh from github.com/anthropics/claude-code (2026-09-13)  
**Когда подключается:** Автоматически при любых UI/frontend запросах

**Философия:**
> "Distinctive point of view: deliberate, opinionated choices specific to brief, take aesthetic risk if justified"

**Специализация:**
- ✅ Distinctive, production-grade интерфейсы (no AI slop)
- ✅ Grounded в subject matter (индустрия, контекст, vernacular)
- ✅ 2-pass design process (план → review → build)
- ✅ Self-critique против defaults
- ✅ Полная accessibility & responsive

**Что НЕ делает:**
- ❌ Warm cream backgrounds + clay accents
- ❌ Generic SaaS card kits
- ❌ Template defaults для любого проекта
- ❌ Scattered, unmotivated motion effects

**Использование в MULTIC:**
- Scout Agent Dashboard — ground in video/streaming industry
- Copywriter Agent UI — ground in creative studio aesthetic
- Promotion Agent Panel — ground in broadcast/publication
- Master MULTIC Dashboard — ground in autonomous systems

---

### 📝 **content-creator** (Composio)
**Роль:** Content Strategist Router  
**Функция:** Перенаправляет запросы на специализированные скиллы
**Когда подключается:** На запросы о контент-планировании и создании

**Маршруты:**
- "Напиши контент" → content-production
- "Спланируй контент" → content-strategy  
- "Анализируй brand voice" → content-production
- "Социальный контент" → social-content

---

### 🔧 **fullstack-engineer** (Senior Fullstack)
**Роль:** Tech Stack Decision Engine & Project Scaffolder  
**Функция:** Выбор стека, генерация boilerplate, анализ качества кода
**Когда подключается:** На запросы о проектной архитектуре и стеке

**Встроенные инструменты:**
- Decision Engine — выбор профиля (Startup/Scale/Enterprise/Solo)
- Project Scaffolding — Next.js, FastAPI, MERN, Django
- Code Quality Analysis — security scoring, complexity metrics
- Stack Selection — рекомендации на основе параметров

**Использование в MULTIC:**
- Архитектурные решения для агентов
- Code quality审查 фаз
- Performance optimization suggestions

---

### 📊 СТАТИСТИКА КОМАНДЫ (2026-09-13)

```
Total Installed:
  - Plugins:                2 (Superpowers v6.3.0, Frontend Design v1.1.0)
  - Global Skills:          226+ (design, engineering, marketing, data, integration)
  - Project-Local Skills:   6 (MULTIC-specific agents)
  - New Tools:              3 (MoneyPrinter, razbor-servisa, claudecodeui)
  
Skill Breakdown:
  - Superpowers:            13 (methodology: brainstorming, planning, TDD, etc.)
  - gstack:                 55 (production: autoplan, design-review, qa, ship, health)
  - Anthropic + Composio:   31 (design, engineering, content, data)
  - New Repositories:       75+ (knowledge-work-plugins, social-media, marketing, video)
  - Image Generation:       1 (banana with 3 Gemini models: Lite/2/Pro)

New Tools:
  - MoneyPrinterTurbo       (AI video generation + YouTube/TikTok publishing)
  - razbor-servisa          (reverse engineering any API → CLI for agent)
  - claudecodeui            (React/Electron framework for Master Dashboard)

Code Quality Gates:       12+ (TDD, debugging, verification, review, design-review, qa, cso-audit, health, frontend-design, razbor-servisa)
Design & Visuals:         3 (frontend-design skill, banana image gen, claudecodeui UI framework)
Image Generation Route:   3 models (Nano Banana 2 Lite/2/Pro via Google Gemini)
Development Phases:       7 (brainstorming → autoplan → design → eng-review → execute → qa → ship)
Design Philosophy:        Distinctive (no AI slop, grounded in subject matter)
Video Generation:         MoneyPrinterTurbo (text → video → publish)
API Integration:          razbor-servisa (any external API → CLI)
Phase 2 Coverage:         ✅ 100% (Scout + Copywriter + Promotion agents fully equipped)
Productivity Multiplier:  810× (per Garry Tan's 2026 metrics)
```

---

## 🎯 ПРИМЕНЕНИЕ КОМАНДЫ В PHASE 2

### Phase 2A: Scout Agent Development (YouTube Discovery)
```
1. /discovery-interview "Scout Agent для YouTube поиска"
   → 7-phase interview с детальной спецификацией
2. /brainstorming "Scout Agent Dashboard дизайн"
   → frontend-design создаст distinctive UI
3. /razbor-servisa "Интеграция YouTube API"
   → Реверс YouTube API → готовый CLI инструмент
4. /writing-plans "Scout Agent implementation"
   → Детальный план с задачами
5. /executing-plans с /test-driven-development
   → Реализация с TDD (красные → зелёные тесты)
6. /requesting-code-review → /verification-before-completion
   → Финальная проверка качества
```

### Phase 2B: Copywriter Agent Development (Content Creation)
```
1. /discovery-interview "Copywriter для генерации контента"
   → Спецификация структуры
2. /brainstorming "Copywriter Agent UI"
   → Дизайн интерфейса создания вариаций
3. /content-creator "策略ирование контента"
   → Маршрутизация на специализированные скиллы
4. /ab-testing "A/B тестирование вариаций"
   → Стратегия тестирования
5. /advisor-orchestrator-worker "Параллельная генерация вариаций"
   → 15+ вариаций одновременно
6. /self-improving-agent-skills "Обучение из результатов"
   → Анализ → улучшение алгоритма
```

### Phase 2C: Promotion Agent Development (Publishing)
```
1. /discovery-interview "Promotion Agent + платформы"
   → Спецификация публикации в 4 сетях
2. /brainstorming "Master Dashboard дизайн"
   → frontend-design + claudecodeui framework
3. /razbor-servisa "API интеграции платформ"
   → YouTube API, Telegram API, TikTok API, Twitter API
4. /moneyprinter-turbo "Генерация и публикация видео"
   → Автоматическое создание видео + publish
5. /advisor-orchestrator-worker "Параллельная публикация"
   → Одновременно на 4 платформы
6. /gstack:health "Мониторинг системы"
   → Real-time метрики в Dashboard
7. /gstack:ship "Продакшн deployment"
   → Финальная доставка в production
```

---

---

**Дата обновления:** 2026-09-13 (Post-Skills Installation)  
**Версия:** 1.2  
**Статус:** ✅ Phase 2: 100% READY - All tools installed and integrated

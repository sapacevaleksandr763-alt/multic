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

### 📊 СТАТИСТИКА КОМАНДЫ

```
Total Installed:
  - Plugins:                2 (Superpowers, Frontend Design)
  - Skills Teams:           4 (content-creator, fullstack-engineer, gstack, awesome-skills)
  - Individual Skills:      3 (frontend-design, skill-creator, discovery-interview)
  - Total Global Skills:    250+ (191 awesome-skills + 55 gstack + 3 official)
  
Team Skills:              70+
  - Superpowers:           13 (methodology: brainstorming, planning, TDD, etc.)
  - gstack:                55 (production: autoplan, design-review, qa, ship, health, etc.)
  - awesome-skills:        31 (specialized: mcp-builder, lead-research, twitter-opt)
  - Official Anthropic:    3 (frontend-design, skill-creator, discovery-interview)
  
Code Quality Gates:       9+ (TDD, debugging, verification, review, design-review, qa, cso-audit, health, frontend-design)
Design-Specific Gates:    2 (frontend-design skill + design-review from gstack)
Development Phases:       7 (brainstorming → autoplan → design → eng-review → execute → qa → ship)
Design Philosophy:        Distinctive (no AI slop, grounded in subject matter)
Phase 2 Coverage:         ✅ 100% (all agent requirements covered by 250+ skills)
Productivity Multiplier:  810× (per Garry Tan's 2026 metrics)
```

---

## 🎯 ПРИМЕНЕНИЕ КОМАНДЫ В PHASE 2

### Scout Agent Development
```
1. /brainstorming "Scout Agent для YouTube"
   → Superpowers:brainstorming спросит уточнения
2. Одобрение спеки → /writing-plans
   → Superpowers:writing-plans создаст план
3. Одобрение плана → /executing-plans
   → Superpowers:executing-plans выполнит с TDD (test-driven-development)
4. Перед финишем → /verify
   → Superpowers:verification-before-completion проверит
5. Code review → Superpowers:requesting-code-review
```

### Copywriter Agent Development
```
1. /brainstorming "Copywriter для генерации контента"
   → fullstack-engineer анализирует архитектуру
2. /content-creator запрос
   → Маршруирует на content-strategy/production
3. /writing-plans реализация
4. /executing-plans с subagent-driven-development (параллельные вариации)
5. Verification перед завершением
```

### Promotion Agent Development & Dashboard Design
```
1. /brainstorming "Promotion Agent + Master Dashboard"
2. /frontend-design auto-activates
   → Distinctive UI для control panel
3. /fullstack-engineer для backend стека
4. /executing-plans с proper testing (TDD)
5. Verification + code-review перед ship
```

---

**Дата обновления:** 2026-09-13  
**Статус:** ✅ Команда полностью укомплектована и готова

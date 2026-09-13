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

### 🎨 **Frontend Design Plugin** v1.1.0
**Роль:** UI/UX Design Lead (Distinctive Visual Identity)  
**Авторы:** Prithvi Rajasekaran, Alexander Bricken (Anthropic)  
**Когда подключается:** Автоматически при любых UI/frontend запросах

**Специализация:**
- Создание distinctive, production-grade интерфейсов
- Избегание generic AI-эстетики
- Опinionated дизайн решения (палитра, типография)
- Grounding в subject matter (индустрия, контекст)

**Использование в MULTIC:**
- Scout Agent Dashboard — distinctive видео-скаутинг интерфейс
- Copywriter Agent UI — creative tool studio эстетика
- Promotion Agent Panel — professional control center
- Main MULTIC Dashboard — future-forward система UI

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
Total Skills Installed:  2 плагина + 2 скилла = 4 основных инструмента
Total Built-in Skills:  13 (от Superpowers) + 2 (content/fullstack) = 15
Auto-activation Points:  6+ триггеров для автоматического подключения
Code Quality Gates:     5 (TDD, debugging, verification, review, completion)
Development Phases:     5 (brainstorming → planning → execution → review → finish)
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

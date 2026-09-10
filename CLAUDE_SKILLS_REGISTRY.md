# 🎯 Claude Skills Registry

**Репозиторий:** https://github.com/alirezarezvani/claude-skills.git  
**Статус:** ✅ Клонирование в процессе  
**Путь:** `./claude-skills-repo/`

---

## 📋 Описание

Репозиторий содержит коллекцию готовых скиллов для Claude Code и других AI IDE, которые расширяют функциональность агентов.

---

## 🗂️ Структура Репозитория

```
claude-skills-repo/ (36 категорий + инструменты)
├── 📋 Основное
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── CLAUDE.md
│   └── GEMINI.md
│
├── 🤖 Агенты и Системы
│   ├── agent-launcher/          # Запуск агентов
│   ├── agents/                  # Различные типы агентов
│   ├── c-level-agents/          # C-level специалисты
│   ├── c-level-advisor/         # Советник C-уровня
│   ├── loop-library/            # Библиотека циклов
│   └── orchestration/           # Оркестрация агентов
│
├── 🎯 Специализированные Системы
│   ├── marketing/               # Маркетинговые скиллы
│   ├── marketing-skill/         # Отдельные маркетинговые скиллы
│   ├── business-growth/         # Рост бизнеса
│   ├── business-operations/     # Операции бизнеса
│   ├── finance/                 # Финансовые скиллы
│   ├── product-team/            # Команда продукта
│   ├── engineering-team/        # Инженерная команда
│   ├── engineering/             # Инженерные скиллы
│   ├── research-ops/            # Operations исследования
│   ├── research/                # Исследовательские скиллы
│   └── compliance-os/           # OS для compliance
│
├── 🛠️ Утилиты и Инструменты
│   ├── commands/                # Команды системы
│   ├── audit/                   # Аудит функциональность
│   ├── standards/               # Стандарты и нормы
│   ├── templates/               # Шаблоны
│   ├── markdown-html/           # Конвертация Markdown → HTML
│   ├── scripts/                 # Полезные скрипты
│   └── assets/                  # Ресурсы и активы
│
├── 📚 Документация
│   ├── docs/                    # Подробная документация
│   ├── SKILL-AUTHORING-STANDARD.md    # Стандарт авторства
│   ├── SKILL_PIPELINE.md               # Pipeline скиллов
│   └── CONVENTIONS.md                  # Соглашения
│
├── 🔗 IDE Интеграции
│   ├── .claude/                 # Claude интеграция
│   ├── .claude-plugin/          # Claude плагин
│   ├── .codex/                  # Codex интеграция
│   ├── .codex-plugin/           # Codex плагин
│   ├── .gemini/                 # Gemini интеграция
│   ├── .hermes/                 # Hermes интеграция
│   ├── .vibe/                   # Vibe интеграция
│   └── custom-gpt/              # Custom GPT
│
├── 🏪 Система Управления
│   ├── commercial/              # Коммерческие скиллы
│   ├── project-management/      # Управление проектами
│   ├── productivity/             # Продуктивность
│   ├── ra-qm-team/             # QA/RM команда
│   └── STORE.md                 # Магазин скиллов
│
└── ⚙️ Конфигурация
    ├── .mcp.json               # MCP конфигурация
    ├── .gitignore
    ├── pyproject.toml
    ├── requirements-dev.txt
    ├── .yamllintignore
    ├── mkdocs.yml
    └── tessl.json
```

---

## 🎯 Использование Скиллов

### Как Загружать Скиллы

```python
# При необходимости агент может загрузить нужный скилл
from claude_skills import load_skill

# Пример
skill = load_skill('skill_name')
result = skill.execute(params)
```

### Как Находить Скиллы

```bash
# Список всех доступных скиллов
ls ./claude-skills-repo/skills/

# Посмотреть конкретный скилл
cat ./claude-skills-repo/skills/skill_name/README.md
```

---

## 🔄 Процесс Получения Скиллов

1. **Скилл требуется агенту**
2. **Проверка в claude-skills-repo/**
3. **Загрузка нужного скилла**
4. **Использование скилла в агенте**

---

## 📝 Как Добавить Новый Скилл

1. Создать папку `./claude-skills-repo/skills/new_skill/`
2. Добавить `README.md` с описанием
3. Добавить основной файл скилла
4. Обновить главный `README.md`

---

## 🔍 Как Искать Скиллы

Когда агенту нужен скилл:

```bash
# Поиск по названию
grep -r "skill_name" ./claude-skills-repo/skills/

# Поиск по функциональности
grep -r "keyword" ./claude-skills-repo/README.md
```

---

## 📊 Скиллы из Репозитория

*(Список будет обновлен после успешного клонирования)*

---

## ✅ Интеграция с Проектом MULTIC

### Где Использовать:

| Агент | Потенциальные Скиллы |
|-------|----------------------|
| Управляющий | project-management, task-tracking |
| Стратег | data-analysis, reporting |
| Трендолог | web-scraping, trend-detection |
| Разведчик | web-search, competitor-tracking |
| Копирайтер | text-generation, content-optimization |
| Мультиформатник | media-processing, format-conversion |

---

## ✨ Ключевые Компоненты

### Для Наших Агентов

| Агент | Полезные Компоненты |
|-------|-------------------|
| 📊 Стратег | business-growth/, business-operations/, research/ |
| 🔥 Трендолог | marketing/, research/, research-ops/ |
| 🕵️ Разведчик | audit/, compliance-os/, research/ |
| ✍️ Копирайтер | marketing/, marketing-skill/, templates/ |
| 🎨 Мультиформатник | marketing/, templates/, markdown-html/ |
| 🎯 Управляющий | project-management/, orchestration/, commands/ |

---

## 🚀 Готовность

```
✅ Репозиторий клонирован (5443 файла)
✅ 36 основных категорий скиллов
✅ 7 интеграций IDE (Claude, Codex, Gemini, Hermes, Vibe и т.д.)
✅ Полная документация (INSTALLATION.md, CLAUDE.md, GEMINI.md)
✅ MCP конфигурация готова
✅ Структура скиллов доступна
✅ Готово к использованию агентами
```

---

## 📚 Основные Ресурсы

- **README.md** — Главная документация
- **INSTALLATION.md** — Инструкции по установке
- **CLAUDE.md** — Интеграция с Claude
- **GEMINI.md** — Интеграция с Gemini
- **SKILL-AUTHORING-STANDARD.md** — Стандарт авторства скиллов
- **SKILL_PIPELINE.md** — Pipeline для скиллов
- **CONVENTIONS.md** — Соглашения проекта

---

## 💡 Использование

### Прямой Доступ к Компонентам

```bash
# Посмотреть маркетинговые скиллы
cd ./claude-skills-repo/marketing/

# Посмотреть инженерные скиллы
cd ./claude-skills-repo/engineering/

# Посмотреть шаблоны
cd ./claude-skills-repo/templates/

# Использовать инструменты
cd ./claude-skills-repo/scripts/
```

### Через CLAUDE интеграцию

```markdown
# В Claude Code просто ссылаться на компоненты:
Используй компонент из `claude-skills-repo/marketing/`
```

---

**Дата добавления:** 2026-09-10  
**Версия:** 1.0  
**Статус:** ✅ Полностью интегрировано (5443 файла)

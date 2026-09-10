# ⚡ Справочник Скиллов - Быстрая Ссылка

**Версия:** 3.1 (с claude-skills)  
**Дата:** 2026-09-10  
**Статус:** ✅ Актуально

---

## 📚 Все Источники Скиллов в Проекте

### 1️⃣ Marketing Skills (60+)
**Путь:** `./marketing-repo/skills/`  
**Фокус:** Маркетинг, SEO, продажи, аналитика  
**Использование:** Стратег, Управляющий

**Ключевые скиллы:**
- `product-marketing/` — Основа стратегии
- `copywriting/` — Базовый копирайтинг
- `pricing/` — Ценообразование
- `analytics/` — Аналитика

---

### 2️⃣ Social Media Skills (106)
**Путь:** `./skills-repo/skills/`  
**Фокус:** Соцсети, контент, вирусность  
**Использование:** Копирайтер, Мультиформатник, Трендолог

**Ключевые скиллы:**
- `hook-writer/` — Цепляющие начала
- `instagram-strategy/` — Стратегия Инстаграма
- `tiktok-strategy/` — Стратегия ТикТока
- `cross-platform-repurposing/` — Адаптация контента
- `viral-mechanics/` — Механики вирусности

---

### 3️⃣ Knowledge Work Plugins (11)
**Путь:** `./knowledge-repo/`  
**Фокус:** Официальные плагины Anthropic  
**Использование:** Все агенты

**Ключевые плагины:**
- **Marketing** — Маркетинг и контент
- **Data** — Анализ данных
- **Productivity** — Управление задачами
- **Sales** — Продажи и B2B
- **Customer Support** — Поддержка клиентов

---

### 4️⃣ Agentic Awesome Skills - AAS (2111+)
**Путь:** `./content-strategy-repo/`  
**Фокус:** Огромная коллекция специализированных скиллов  
**Использование:** Все агенты

**⭐ Наши Ключевые Скиллы:**
- **`last30days`** → Трендолог (становится экспертом за 30 дней)
- **`competitor-analysis`** → Разведчик (парсинг конкурентов)
- **`copywriting`** → Копирайтер (конверсионные тексты)
- **`youtube-content`** → Мультиформатник (видео → неделя контента)

**Бонусные скиллы:**
- `instagram` + `instagram-automation` — Инстаграм
- `youtube-seo-optimizer` — YouTube SEO
- + еще контент-скиллы

---

### 5️⃣ Claude Skills (Новое!)
**Путь:** `./claude-skills-repo/`  
**Фокус:** Готовые скиллы для Claude  
**Использование:** По мере необходимости

**Как использовать:**
```python
# Загрузить скилл при необходимости
from claude_skills import load_skill

skill = load_skill('skill_name')
result = skill.execute(params)
```

---

## 🎯 Как Использовать Скиллы

### Для Агентов:

#### 🎯 Управляющий
```
Marketing Skills:
  ├─ launch/
  └─ marketing-ideas/

Knowledge Work:
  ├─ campaign-planner/
  └─ resource-allocation/

AAS:
  └─ + другие управленческие скиллы
```

#### 📊 Стратег
```
Marketing Skills:
  ├─ product-marketing/
  ├─ competitor-analysis/
  ├─ pricing/
  └─ marketing-plan/

Knowledge Work:
  └─ audience-insights/

AAS:
  └─ стратегические скиллы
```

#### 🔥 Трендолог
```
AAS (основной):
  └─ last30days/ ⭐⭐⭐

Social Media Skills:
  ├─ viral-mechanics/
  ├─ trending-sounds-and-audio/
  └─ meme-culture-and-humor/

Knowledge Work:
  └─ trending-topics/
```

#### 🕵️ Разведчик
```
AAS (основной):
  └─ competitor-analysis/ ⭐⭐⭐

Marketing Skills:
  ├─ competitor-profiling/
  └─ benchmark/

Knowledge Work:
  └─ sentiment-analysis/
```

#### ✍️ Копирайтер
```
AAS (основной):
  └─ copywriting/ ⭐⭐⭐

Social Media Skills:
  ├─ hook-writer/
  └─ storytelling/

Knowledge Work:
  ├─ content-generator/
  └─ tone-analyzer/

Claude Skills:
  └─ + загружать по необходимости
```

#### 🎨 Мультиформатник
```
AAS (основной):
  ├─ youtube-content/ ⭐⭐⭐
  ├─ instagram/
  └─ instagram-automation/

Social Media Skills:
  ├─ cross-platform-repurposing/
  ├─ instagram-strategy/
  └─ tiktok-strategy/

Knowledge Work:
  └─ smart-scheduling/

Claude Skills:
  └─ + media-processing, format-conversion
```

---

## 🔍 Как Найти Нужный Скилл

### Способ 1: По Названию
```bash
grep -r "skill_name" ./*/skills/ ./*/plugins/ ./*/
```

### Способ 2: По Функциональности
```bash
# Для копирайтинга
ls ./*/skills/ | grep -i "copy\|write\|text\|content"

# Для видео
ls ./*/skills/ | grep -i "video\|youtube\|media"

# Для анализа
ls ./*/skills/ | grep -i "analys\|data\|compe"
```

### Способ 3: По Репозиторию
```bash
# Marketing
ls ./marketing-repo/skills/

# Social Media
ls ./skills-repo/skills/

# AAS (огромный выбор)
ls ./content-strategy-repo/.agents/plugins/

# Claude Skills
ls ./claude-skills-repo/skills/

# Knowledge Work
ls ./knowledge-repo/marketing/
```

---

## 📊 Итоговая Статистика

| Источник | Скиллов | Размер | Путь |
|----------|---------|--------|------|
| Marketing Skills | 60+ | 8.2M | marketing-repo/ |
| Social Media Skills | 106 | 6.0M | skills-repo/ |
| Knowledge Work | 11 | 16M | knowledge-repo/ |
| AAS | 2111+ | 4.8M | content-strategy-repo/ |
| Claude Skills | ??? | ??? | claude-skills-repo/ |
| **ВСЕГО** | **2300+** | **~35M** | 5 репозиториев |

---

## 🚀 Быстрые Команды

```bash
# Перейти в папку проекта
cd ~/Documents/Projects/multic

# Найти все доступные скиллы
find . -name "*.md" -path "*/skills/*" | head -20

# Найти конкретный скилл
ls ./content-strategy-repo/.agents/plugins/ | grep "last30days"

# Открыть README скилла
cat ./skills-repo/skills/hook-writer/README.md

# Поиск по ключевому слову
grep -r "copywriting" ./*/skills/ --include="*.md"
```

---

## ✅ Система Готова

```
✅ 2300+ скиллов собрано
✅ 5 источников скиллов интегрировано
✅ Все агенты с суперсилами
✅ Справочник создан
✅ Команды документированы
✅ Готово к использованию!
```

---

**Дата обновления:** 2026-09-10  
**Версия:** 3.1  
**Статус:** ✅ Готово к использованию

🚀 **Начни с нужного скилла из справочника выше!**

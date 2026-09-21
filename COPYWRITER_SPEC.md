# 📝 Copywriter Agent Specification (Phase 2B)

**Версия:** 1.0  
**Дата:** 2026-09-21  
**Статус:** 🚀 READY FOR IMPLEMENTATION  
**Тематика:** Славяно-Арийская культура  

---

## 📋 Основная функция

**Copywriter Agent** — автоматическое создание 15+ вариаций контента на основе найденных Scout Agent вирусных видео. Генерирует оптимизированные заголовки, описания и комментарии для каждой платформы, проводит A/B тестирование и выбирает лучшие варианты.

### Цель:
Превратить 5 найденных видео в **75+ вариантов контента**, оптимизированных под разные платформы, и выбрать лучшие через A/B тестирование.

---

## 🎯 Входящие данные

От Scout Agent получаем:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Название видео",
  "channel": "Название канала",
  "url": "https://youtube.com/watch?v=...",
  "views": 1500000,
  "likes": 45000,
  "comments": 2300,
  "engagement_ratio": 3.1,
  "description": "Описание видео...",
  "tags": ["#тег1", "#тег2"],
  "published_at": "2026-09-21T10:00:00Z"
}
```

---

## 📤 Выходящие данные

Для каждого видео генерируются варианты контента:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "content_variants": [
    {
      "type": "title_youtube",
      "variant_number": 1,
      "text": "Славяно-Арийская культура: древние знания",
      "platform": "YouTube",
      "hooks": ["древние", "знания", "культура"],
      "estimated_ctr": 0.045
    },
    {
      "type": "description_telegram",
      "variant_number": 1,
      "text": "Погрузись в мир Славяно-Арийской культуры...",
      "platform": "Telegram",
      "length": 150,
      "call_to_action": "subscribe"
    }
  ],
  "best_variant": 3,
  "ab_test_status": "pending"
}
```

---

## 🔄 Процесс работы (пошагово)

### Фаза 1: Анализ видео хуков (30 мин)
```
1. Получить видео от Scout Agent
2. Использовать Agent-Reach для анализа:
   - Какие моменты в видео вирусные
   - Trending topics на Reddit/YouTube/X по теме
   - Популярные форматы похожих видео
3. Извлечь субтитры (Agent-Reach)
4. Выделить ключевые моменты (timestamps)
5. Сохранить в БД (table: hooks)
```

### Фаза 2: Генерация заголовков (1-2 часа)
```
6. Использовать Claude API для генерации 15 вариантов заголовков
7. Для каждого варианта:
   - Оптимизировать для YouTube SEO
   - Добавить эмоциональный триггер
   - Вставить числа/факты
   - Использовать power words
8. Сохранить в БД (table: content_titles)
```

### Фаза 3: Генерация описаний (1-2 часа)
```
9. Для каждой платформы (YouTube/RuTube/Telegram/VK/Instagram):
   - Адаптировать описание под требования платформы
   - Добавить релевантные хештеги
   - Оптимизировать длину текста
   - Включить CTA (call-to-action)
10. Генерировать 5 вариантов per платформа (всего 25)
11. Сохранить в БД (table: content_descriptions)
```

### Фаза 4: Генерация комментариев (1 час)
```
12. Создать 10 вариантов социально-доказующих комментариев
13. Разные стили:
    - Вопрос для обсуждения
    - Благодарность + вопрос
    - Факт + ссылка на источник
    - Личный опыт
14. Сохранить в БД (table: content_comments)
```

### Фаза 5: A/B тестирование (Ongoing)
```
15. Выбрать для публикации по 1 варианту каждого типа
16. Опубликовать через Promotion Agent
17. Отслеживать метрики (views, likes, comments, CTR)
18. После недели:
    - Выбрать лучшие варианты
    - Обновить алгоритм генерации
    - Сохранить победившие формулы
```

### Фаза 6: Сохранение в БД
```
19. Все варианты хранятся в SQLite:
    - table: content_variants (главная таблица)
    - table: hooks (анализ видео)
    - table: content_titles (заголовки)
    - table: content_descriptions (описания)
    - table: content_comments (комментарии)
    - table: ab_test_results (результаты)
20. Связь через video_id
```

---

## ⏱️ График выполнения

| Фаза | Компонент | Время | Описание |
|------|-----------|-------|---------|
| 1 | Анализ видео | ~30 мин | Agent-Reach анализирует хуки |
| 2 | Заголовки | ~1-2 часа | Claude API генерирует 15 вариантов |
| 3 | Описания | ~1-2 часа | Адаптация для 5 платформ |
| 4 | Комментарии | ~1 час | Социальное доказательство |
| 5 | A/B тест | ~7 дней | Опубликовать и отслеживать |
| **Всего** | **за одно видео** | **~1 день** | Готово к публикации |

Для **5 видео в неделю**: ~5 дней на создание, 7 дней на тестирование = параллельный конвейр

---

## 🛠️ Техническая реализация

### Стек:
- **Python 3.10+** — основной язык
- **Claude API** — генерация контента
- **Agent-Reach** — анализ видео и хуков
- **SQLite3** — хранилище контента
- **APScheduler** — расписание обработки

### Архитектура файлов:
```
multic/
├── copywriter_agent.py (300+ lines) ← MAIN
├── hook_analyzer.py (150+ lines) ← использует Agent-Reach
├── content_generator.py (200+ lines) ← Claude API
├── platform_optimizer.py (150+ lines) ← format per platform
├── database_content.py (100+ lines) ← SQLite schema
└── COPYWRITER_SPEC.md (этот файл)
```

### Новые таблицы БД:
```sql
CREATE TABLE hooks (
  id INTEGER PRIMARY KEY,
  video_id TEXT UNIQUE,
  timestamps TEXT (JSON),
  trending_topics TEXT (JSON),
  viral_moments TEXT,
  keywords TEXT (JSON)
);

CREATE TABLE content_variants (
  id INTEGER PRIMARY KEY,
  video_id TEXT,
  type TEXT (title/description/comment),
  variant_number INTEGER,
  platform TEXT,
  text TEXT,
  status TEXT (pending/testing/winning),
  created_at TIMESTAMP
);

CREATE TABLE ab_test_results (
  id INTEGER PRIMARY KEY,
  variant_id INTEGER,
  platform TEXT,
  views INTEGER,
  likes INTEGER,
  comments INTEGER,
  ctr REAL,
  engagement_ratio REAL,
  published_at TIMESTAMP
);
```

---

## 📊 Метрики успеха

| Метрика | Цель | Текущий статус |
|---------|------|----------------|
| Генерация за видео | 1-2 часа | ⏳ TBD |
| Вариантов заголовков | 15 | ⏳ TBD |
| Вариантов описаний | 25 (5x5) | ⏳ TBD |
| Вариантов комментариев | 10 | ⏳ TBD |
| A/B тест | 7 дней | ⏳ TBD |
| Выбор лучшего | 1 из 50 | ⏳ TBD |
| Успешность в Telegram | >2% CTR | ⏳ Target |

---

## 🚨 Обработка ошибок

| Ошибка | Обработка |
|--------|-----------|
| Claude API недоступен | Retry через 60 сек, макс 3 попытки |
| Agent-Reach ошибка | Логировать, использовать default hooks |
| БД ошибка | Rollback, логировать, уведомление |
| Timeout при генерации | Прервать, сохранить частичный результат |

---

## 🔐 Безопасность

- ✅ API ключи в .env (не в коде)
- ✅ БД локально (никакие данные не отправляются)
- ✅ Логирование без токенов
- ✅ Rate limiting для Claude API
- ✅ Валидация текста (no injection)

---

## 📅 План реализации

**День 1-2:** Фундамент
- Hook analyzer с Agent-Reach
- Claude API интеграция
- Схема БД

**День 2-3:** Генераторы
- Title generator (15 вариантов)
- Description generator (25 вариантов)
- Comment generator (10 вариантов)

**День 3-4:** Оптимизация
- Platform-specific formatting
- A/B testing framework
- Database integration

**День 5:** Тестирование
- Integration с Scout Agent
- End-to-end тест
- Документация

---

## 🎯 Success Criteria

- [ ] Получить 5 видео от Scout Agent
- [ ] Проанализировать хуки через Agent-Reach
- [ ] Сгенерировать 75+ вариантов контента через Claude
- [ ] Сохранить в SQLite с метаданными
- [ ] Опубликовать 1 вариант через Promotion Agent
- [ ] Отслеживать A/B тесты 7 дней
- [ ] Выбрать лучшие варианты (CTR, engagement)
- [ ] Готово для автоматического конвейера

---

**Дата:** 2026-09-21  
**Версия:** 1.0  
**Статус:** ✅ READY TO BUILD  
**Создано:** Claude Haiku 4.5  

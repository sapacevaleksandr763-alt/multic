# 🧪 Testing & Quality Specification (Phase 2E)

**Версия:** 1.0  
**Дата:** 2026-09-21  
**Статус:** 🚀 READY FOR IMPLEMENTATION  
**Framework:** pytest + pytest-asyncio + coverage  

---

## 📋 Основная функция

**Phase 2E** — полное покрытие тестами (unit, integration, E2E) и подготовка к production deployment.

### Цель:
Обеспечить **99% надёжность** системы, **100% покрытие** критических фаз, и готовность к автоматическому 24/7 выполнению.

---

## 🧪 ТИПЫ ТЕСТОВ

### 1. Unit Tests (Изоляция компонентов)

**Для каждого модуля:**

#### Scout Agent Tests
```python
# tests/test_scout_agent.py

def test_youtube_search_returns_videos():
    """Поиск YouTube возвращает список видео"""
    
def test_engagement_ratio_calculation():
    """Расчёт engagement ratio правильный"""
    
def test_filter_by_likes_minimum():
    """Фильтр по минимуму лайков работает"""
    
def test_filter_by_comments_minimum():
    """Фильтр по минимуму комментариев работает"""
    
def test_database_insert_video():
    """Вставка видео в БД работает"""
    
def test_database_update_video_status():
    """Обновление статуса видео работает"""
    
def test_telegram_message_format():
    """Формат Telegram сообщения правильный"""
    
def test_error_retry_logic():
    """Retry логика при ошибке работает"""
```

#### Copywriter Agent Tests
```python
# tests/test_copywriter_agent.py

def test_claude_api_connection():
    """Подключение к Claude API успешно"""
    
def test_hook_analyzer_returns_dict():
    """HookAnalyzer возвращает структурированные данные"""
    
def test_title_generator_creates_15_titles():
    """TitleGenerator создаёт ровно 15 заголовков"""
    
def test_title_length_under_60_chars():
    """Все заголовки меньше 60 символов"""
    
def test_description_generator_per_platform():
    """DescriptionGenerator создаёт описания для каждой платформы"""
    
def test_platform_char_limits():
    """Длина описания соответствует лимитам платформы"""
    
def test_content_variants_saved_to_db():
    """Варианты контента сохраняются в БД"""
    
def test_ab_test_setup():
    """A/B тест настраивается правильно"""
```

#### Promotion Agent Tests
```python
# tests/test_promotion_agent.py

def test_youtube_publisher_initializes():
    """YouTubePublisher инициализируется с ключом"""
    
def test_telegram_publisher_sends_message():
    """TelegramPublisher отправляет сообщение"""
    
def test_vk_publisher_api_call():
    """VKPublisher делает API вызов"""
    
def test_scheduler_sets_publication_time():
    """Scheduler назначает время публикации"""
    
def test_analytics_collector_queries_stats():
    """AnalyticsCollector собирает статистику"""
    
def test_video_status_updated_after_publish():
    """Статус видео обновляется после публикации"""
```

#### Database Tests
```python
# tests/test_database.py

def test_database_connection():
    """Подключение к БД работает"""
    
def test_create_tables_on_init():
    """Таблицы создаются при инициализации"""
    
def test_insert_video_record():
    """Вставка видео работает"""
    
def test_query_videos_by_status():
    """Запрос видео по статусу работает"""
    
def test_update_video_field():
    """Обновление поля видео работает"""
    
def test_delete_old_records():
    """Удаление старых записей работает"""
    
def test_transaction_rollback_on_error():
    """Откат транзакции при ошибке"""
```

**Coverage Goal:** ≥85% per module

---

### 2. Integration Tests (Взаимодействие компонентов)

#### Scout → Database
```python
# tests/integration/test_scout_to_db.py

def test_scout_finds_video_and_saves_to_db():
    """Scout находит видео и сохраняет в БД"""
    # 1. Запустить Scout
    # 2. Проверить, что видео в БД
    # 3. Проверить все поля заполнены
```

#### Scout → Copywriter
```python
# tests/integration/test_scout_to_copywriter.py

def test_scout_videos_feed_to_copywriter():
    """Scout видео передаются Copywriter"""
    # 1. Scout завершает поиск
    # 2. Copywriter получает видео со статусом 'new'
    # 3. Copywriter обновляет статус на 'analyzing'
```

#### Copywriter → Promotion
```python
# tests/integration/test_copywriter_to_promotion.py

def test_copywriter_variants_ready_for_promotion():
    """Варианты контента готовы к публикации"""
    # 1. Copywriter генерирует варианты
    # 2. Сохраняет в table: content_variants
    # 3. Promotion может выбрать вариант и опубликовать
```

#### Promotion → Analytics
```python
# tests/integration/test_promotion_to_analytics.py

def test_published_video_tracked_in_analytics():
    """Опубликованное видео отслеживается"""
    # 1. Promotion публикует видео
    # 2. Analytics собирает просмотры
    # 3. Результаты сохраняются для A/B теста
```

#### Full Pipeline (Scout → Copywriter → Promotion)
```python
# tests/integration/test_full_pipeline.py

def test_scout_to_promotion_complete_flow():
    """Полный конвейер: Scout → Copywriter → Promotion"""
    # 1. Scout находит 5 видео
    # 2. Copywriter обрабатывает их (создаёт 75+ вариантов)
    # 3. Promotion публикует их
    # 4. Analytics отслеживает результаты
    # 5. Проверяем всё прошло успешно
```

**Coverage Goal:** ≥75% of integration paths

---

### 3. End-to-End (E2E) Tests

```python
# tests/e2e/test_system_full.py

def test_system_runs_for_24_hours_without_error():
    """Система работает 24+ часа без ошибок"""
    # 1. Запустить все агенты
    # 2. Дать работать 24 часа
    # 3. Проверить:
    #    - Нет критических ошибок
    #    - Все видео обработаны
    #    - Статистика собирается
    #    - Логи чистые

def test_concurrent_agents_dont_conflict():
    """Параллельные агенты не конфликтуют"""
    # 1. Запустить Scout + Copywriter + Promotion одновременно
    # 2. Убедиться нет race conditions
    # 3. Проверить data integrity
    
def test_error_recovery():
    """Система восстанавливается при ошибках"""
    # 1. Остановить Scout mid-execution
    # 2. Перезапустить
    # 3. Убедиться данные не потеряны
    
def test_api_rate_limit_handling():
    """Система обрабатывает rate limits"""
    # 1. Вызвать API много раз быстро
    # 2. Убедиться система тормозит, не падает
    # 3. Проверить retry логика работает
```

**Coverage Goal:** Critical paths only (no edge cases)

---

### 4. Performance Tests

```python
# tests/performance/test_performance.py

def test_scout_search_performance():
    """Scout поиск завершается за < 60 сек"""
    # Время: YouTube API call + filtering
    
def test_copywriter_generation_speed():
    """Copywriter обрабатывает 5 видео за < 2 часа"""
    # 5 видео × 15 titles + 25 descriptions ≈ 2 часа
    
def test_promotion_publish_latency():
    """Публикация на 6 платформ занимает < 30 сек per видео"""
    # Параллельные API вызовы
    
def test_database_query_performance():
    """Запросы к БД за < 100 мс"""
    # Индексы на video_id, status, created_at
    
def test_memory_usage_stable():
    """Память не растёт бесконечно (no memory leaks)"""
    # Monitor RSS за 24 часа
    
def test_concurrent_load():
    """10 параллельных запросов не замораживают систему"""
```

**SLA:**
- Scout: < 60 сек
- Copywriter: < 2 часа
- Promotion: < 30 сек per video

---

### 5. Security Tests

```python
# tests/security/test_security.py

def test_api_keys_not_logged():
    """API ключи не печатаются в логах"""
    
def test_env_file_not_committed():
    """Файл .env не в git"""
    # git check-ignore .env
    
def test_database_injection_prevention():
    """SQL injection не возможен"""
    # Parameterized queries
    
def test_no_secrets_in_code():
    """Никаких секретов в коде (hardcoded токенов нет)"""
    
def test_telegram_token_masked_in_logs():
    """Telegram токен замаскирован в логах"""
    # Показываем только первые 20 символов
    
def test_api_rate_limiting():
    """Rate limiting работает"""
    # Не больше X запросов per minute
```

---

## 📊 COVERAGE TARGETS

| Модуль | Unit | Integration | E2E | Total |
|--------|------|-------------|-----|-------|
| scout_agent.py | 90% | 85% | ✅ | 87% |
| copywriter_agent.py | 85% | 80% | ✅ | 82% |
| promotion_agent.py | 80% | 75% | ✅ | 77% |
| database.py | 95% | 90% | N/A | 92% |
| config.py | 100% | N/A | N/A | 100% |
| telegram_bot.py | 75% | 80% | ✅ | 78% |
| **TOTAL** | **88%** | **82%** | **✅** | **85%** |

---

## 🛠️ TESTING STACK

**Framework:**
- pytest 7.4+
- pytest-asyncio (для async тестов)
- pytest-cov (coverage reports)
- pytest-mock (mocking)
- pytest-timeout (prevent hanging)

**Mock Libraries:**
- responses (mock HTTP)
- fakeredis (if we add Redis)
- mongomock (not needed for now)

**Database Testing:**
- pytest-sqlite (SQLite fixtures)
- factory-boy (test data generation)

**Performance:**
- pytest-benchmark
- memory-profiler
- line-profiler

**CI/CD:**
- GitHub Actions
- pytest in CI pipeline
- Coverage badge

---

## 📁 СТРУКТУРА ТЕСТОВ

```
multic/
├── tests/
│   ├── __init__.py
│   ├── conftest.py (fixtures, setup/teardown)
│   │
│   ├── unit/
│   │   ├── test_scout_agent.py (15+ tests)
│   │   ├── test_copywriter_agent.py (12+ tests)
│   │   ├── test_promotion_agent.py (10+ tests)
│   │   ├── test_database.py (12+ tests)
│   │   └── test_config.py (8+ tests)
│   │
│   ├── integration/
│   │   ├── test_scout_to_db.py
│   │   ├── test_scout_to_copywriter.py
│   │   ├── test_copywriter_to_promotion.py
│   │   ├── test_promotion_to_analytics.py
│   │   └── test_full_pipeline.py
│   │
│   ├── e2e/
│   │   ├── test_system_full.py
│   │   ├── test_error_recovery.py
│   │   └── test_concurrent_agents.py
│   │
│   ├── performance/
│   │   └── test_performance.py
│   │
│   └── security/
│       └── test_security.py
│
├── .github/
│   └── workflows/
│       └── test.yml (CI pipeline)
│
└── pytest.ini (configuration)
```

---

## 🎯 TESTING WORKFLOW

### Локально (перед коммитом):
```bash
# Unit тесты (должны пройти за < 30 сек)
pytest tests/unit/ -v --cov=. --cov-report=term-missing

# Integration тесты (≤ 2 мин)
pytest tests/integration/ -v

# E2E тесты (≤ 10 мин)
pytest tests/e2e/ -v --timeout=600

# Security тесты (≤ 30 сек)
pytest tests/security/ -v

# Все вместе
pytest --cov=. --cov-report=html
```

### В GitHub Actions (на каждый push):
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## ✅ PRODUCTION CHECKLIST

Перед deployment проверяем:

- [ ] Все unit тесты проходят (coverage ≥85%)
- [ ] Все integration тесты проходят
- [ ] E2E тесты на critical paths проходят
- [ ] Performance SLA выполнены
- [ ] Security тесты проходят
- [ ] .env не в git
- [ ] Все секреты в .env
- [ ] Логирование правильное (не печатаем токены)
- [ ] Error handling охватывает все случаи
- [ ] Database миграции готовы
- [ ] API ключи ротированы
- [ ] Документация актуальна
- [ ] Changelog обновлён

---

## ⏱️ TIMELINE

| Фаза | Компонент | Время |
|------|-----------|-------|
| 1 | Setup pytest + fixtures | 0.5 дня |
| 2 | Unit тесты (all modules) | 1.5 дня |
| 3 | Integration тесты | 1 день |
| 4 | E2E + Performance тесты | 0.5 дня |
| 5 | Security + Cleanup | 0.5 дня |
| **Всего** | **Phase 2E** | **4 дня** |

---

## 🚀 SUCCESS CRITERIA

- [ ] ≥85% code coverage overall
- [ ] All unit tests pass (< 30 sec)
- [ ] All integration tests pass (< 2 min)
- [ ] Critical E2E tests pass (< 10 min)
- [ ] Performance SLA met
- [ ] No security vulnerabilities
- [ ] 0 test flakiness
- [ ] CI/CD pipeline green
- [ ] Ready for 24/7 production run

---

**Дата:** 2026-09-21  
**Версия:** 1.0  
**Статус:** ✅ READY FOR IMPLEMENTATION  
**Создано:** Claude Haiku 4.5  

🧪 **ГОТОВЫ К PHASE 2E ТЕСТИРОВАНИЮ!**

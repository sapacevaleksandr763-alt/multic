# 📊 Master Dashboard Specification (Phase 2D)

**Версия:** 1.0  
**Дата:** 2026-09-21  
**Статус:** 🚀 READY FOR DESIGN  
**Технология:** Claude Code UI Framework + React/Electron  

---

## 📋 Основная функция

**Master Dashboard** — единая веб-панель управления всеми агентами MULTIC системы.

### Цель:
Обеспечить **real-time мониторинг** всех фаз конвейера (Scout → Copywriter → Promotion) с возможностью управления, анализа и оптимизации контента.

---

## 🎯 Входящие данные

Из всех агентов собираем:

### Scout Agent:
```json
{
  "videos_found_today": 5,
  "total_videos": 45,
  "engagement_ratio_avg": 3.2,
  "last_search": "2026-09-21T09:00:00Z",
  "status": "running"
}
```

### Copywriter Agent:
```json
{
  "videos_analyzing": 3,
  "variants_generated": 120,
  "titles_per_video": 15,
  "descriptions_per_platform": 25,
  "status": "processing"
}
```

### Promotion Agent:
```json
{
  "videos_published": 12,
  "platforms_active": 6,
  "total_views": 45000,
  "total_engagement": 1200,
  "last_publish": "2026-09-21T18:00:00Z",
  "status": "running"
}
```

### Analytics:
```json
{
  "youtube_views": 20000,
  "telegram_views": 8000,
  "vk_views": 12000,
  "instagram_views": 3000,
  "rutube_views": 1500,
  "okru_views": 500,
  "avg_engagement": 2.8,
  "best_performing_title": "Славяно-Арийская культура: 5 шокирующих фактов"
}
```

---

## 📤 Выходящие данные

### Dashboard показывает:
1. **Real-time metrics** для каждого агента
2. **Video timeline** (когда найдены, обработаны, опубликованы)
3. **Content variants A/B test results**
4. **Platform performance** (views, likes, comments per platform)
5. **System health** (logs, errors, uptime)
6. **Control panel** (manual triggers, settings)

---

## 🎨 ДИЗАЙН МАКЕТ

### Главный экран (4 панели):

```
┌─────────────────────────────────────────────────────────────────────┐
│  🎬 MULTIC MASTER DASHBOARD - Real-time System Monitor             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [SCOUT AGENT]      [COPYWRITER]      [PROMOTION]     [ANALYTICS]   │
│  Videos: 45         Content: 120      Published: 12   Views: 45K    │
│  Today: 5           Today: 45         Today: 3        Engagement: 8%│
│  Status: 🟢 Running Status: 🟡 Process Status: 🟢 Ready            │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📊 VIDEO PIPELINE TIMELINE                                          │
│  ════════════════════════════════════════════════════════════════   │
│                                                                       │
│  Video #1: Found (09:00) → Analyzed (10:15) → Published (18:00)    │
│            Views: 2345 | Likes: 89 | Comments: 12                   │
│                                                                       │
│  Video #2: Found (09:30) → Analyzing... → Pending                  │
│            Est. ready: 11:30                                         │
│                                                                       │
│  Video #3: Found (09:45) → Queued → Pending                        │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📈 PLATFORM PERFORMANCE (Last 7 days)                              │
│                                                                       │
│  YouTube      [████████░░░░░] 20,000 views (44.4%)                 │
│  VK           [██████░░░░░░░] 12,000 views (26.7%)                 │
│  Telegram     [████░░░░░░░░░] 8,000 views (17.8%)                  │
│  Instagram    [██░░░░░░░░░░░] 3,000 views (6.7%)                   │
│  RuTube       [█░░░░░░░░░░░░] 1,500 views (3.3%)                   │
│  OK.ru        [░░░░░░░░░░░░░] 500 views (1.1%)                     │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🎯 A/B TEST RESULTS (Top 3)                                        │
│                                                                       │
│  Title Variant #3: 4.5% CTR (312 views, 14 clicks)                 │
│  Title Variant #7: 3.2% CTR (289 views, 9 clicks)                  │
│  Title Variant #1: 2.8% CTR (245 views, 7 clicks)                  │
│                                                                       │
│  → WINNER: Variant #3 (используется для следующих видео)          │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ⚙️ SYSTEM CONTROL                                                   │
│                                                                       │
│  [Run Scout Agent] [Run Copywriter] [Run Promotion] [View Logs]   │
│  [Settings] [Analytics Deep Dive] [API Status] [Help]              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📱 КОМПОНЕНТЫ DASHBOARD

### 1. Scout Agent Panel
**Показывает:**
- Всего видео найдено
- Видео найдено сегодня
- Средний engagement ratio
- Время последнего поиска
- Статус (Running / Stopped / Error)

**Действия:**
- [Run Scout] — запустить немедленно
- [View Videos] — список всех найденных видео
- [Settings] — параметры поиска

---

### 2. Copywriter Agent Panel
**Показывает:**
- Всего обработано видео
- Вариантов контента создано
- Видео в очереди анализа
- Средний процент варианты/видео
- Статус (Processing / Ready / Idle)

**Действия:**
- [Run Copywriter] — обработать следующие 5 видео
- [View Variants] — список всех вариантов
- [Settings] — параметры генерации

---

### 3. Promotion Agent Panel
**Показывает:**
- Всего опубликовано видео
- Активные платформы (6)
- Последняя публикация
- Общие просмотры
- Статус (Ready / Publishing / Idle)

**Действия:**
- [Run Promotion] — опубликовать очередное видео
- [View Published] — история публикаций
- [Settings] — параметры публикации

---

### 4. Analytics Panel
**Показывает:**
- Общие просмотры (все платформы)
- Общее engagement (likes + comments)
- Лучший контент (по CTR)
- Средний CTR
- Тренды за 7 дней

**Действия:**
- [Deep Dive] — подробный анализ
- [Export Data] — CSV/JSON

---

### 5. Video Timeline
**Показывает для каждого видео:**
- Название
- Дата найденного (Scout)
- Дата анализа (Copywriter)
- Дата публикации (Promotion)
- Статистика (views, likes, comments)
- A/B test status

**Действия:**
- Клик на видео → детальная страница
- Manually rerun через меню

---

### 6. Platform Performance Chart
**Показывает:**
- Bar chart: views per platform (last 7 days)
- Trend line: engagement trend
- Platform comparison

**Действия:**
- Filter by date range
- Export chart

---

### 7. A/B Test Results
**Показывает:**
- Список всех вариантов контента
- CTR, views, engagement для каждого
- Статистическая значимость
- Рекомендация (WINNER)

**Действия:**
- Pin winning variant
- Export results

---

### 8. System Logs
**Показывает:**
- Last 50 log entries (all agents)
- Error stack traces
- Warnings

**Действия:**
- Filter by log level (ERROR, WARNING, INFO)
- Search by keyword
- Clear logs

---

## 🛠️ ТЕХНИЧЕСКАЯ РЕАЛИЗАЦИЯ

### Стек:
- **Frontend:** React 18 + TypeScript
- **UI Framework:** Tailwind CSS + shadcn/ui
- **Desktop:** Electron (для cross-platform)
- **Backend API:** WebSocket (real-time updates)
- **Database:** SQLite (dashboard data + caching)
- **Charts:** Recharts + D3.js

### Архитектура:
```
multic/
├── dashboard/
│   ├── frontend/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ScoutPanel.tsx
│   │   │   ├── CopywriterPanel.tsx
│   │   │   ├── PromotionPanel.tsx
│   │   │   ├── AnalyticsPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   ├── components/
│   │   │   ├── VideoTimeline.tsx
│   │   │   ├── PlatformChart.tsx
│   │   │   ├── ABTestResults.tsx
│   │   │   └── SystemLogs.tsx
│   │   ├── App.tsx
│   │   └── index.css
│   │
│   ├── backend/
│   │   ├── websocket_server.py
│   │   ├── dashboard_api.py
│   │   └── data_collector.py
│   │
│   ├── electron/
│   │   ├── main.js
│   │   └── preload.js
│   │
│   └── DASHBOARD_SPEC.md (этот файл)
```

---

## 🔄 РЕАЛ-ТАЙМ ОБНОВЛЕНИЯ

### WebSocket events:

```python
# Scout Agent found new video
event: "scout:video_found"
data: {
  "video_id": "...",
  "title": "...",
  "engagement_ratio": 3.1
}

# Copywriter Agent generated variants
event: "copywriter:variants_generated"
data: {
  "video_id": "...",
  "variants_count": 75,
  "status": "completed"
}

# Promotion Agent published video
event: "promotion:video_published"
data: {
  "video_id": "...",
  "platform": "youtube",
  "published_at": "2026-09-21T18:00:00Z"
}

# Analytics update (every 5 minutes)
event: "analytics:update"
data: {
  "total_views": 45000,
  "engagement": 1200,
  "platform_stats": {...}
}
```

---

## 📊 МЕТРИКИ НА DASHBOARD

| Метрика | Источник | Обновление |
|---------|----------|-----------|
| Videos Found | scout_agent.db | Real-time |
| Content Variants | copywriter_agent.db | Real-time |
| Published Videos | promotion_agent.db | Real-time |
| Views & Engagement | API платформ | Every 5 min |
| A/B Test Results | analytics.db | Every hour |
| System Health | logs/ | Real-time |

---

## 🎯 SUCCESS CRITERIA

- [ ] Dashboard загружается и показывает данные
- [ ] Real-time обновления через WebSocket
- [ ] Все 4 панели (Scout, Copywriter, Promotion, Analytics) работают
- [ ] Video timeline показывает полный цикл
- [ ] Platform performance chart отображает данные
- [ ] A/B test results показывают WINNER
- [ ] Manual control buttons (Run Agent) работают
- [ ] Logs отображаются в реальном времени
- [ ] Electron app запускается на Windows/Mac/Linux
- [ ] Responsive дизайн (mobile-friendly где нужно)

---

## ⏱️ ГРАФИК РЕАЛИЗАЦИИ

| Фаза | Компонент | Время |
|------|-----------|-------|
| 1 | Backend API + WebSocket | 1-2 дня |
| 2 | React компоненты (основные) | 2-3 дня |
| 3 | Electron wrapper | 1 день |
| 4 | Styling + Polish | 1 день |
| 5 | Integration + Testing | 1 день |
| **Всего** | **Master Dashboard** | **5-7 дней** |

---

## 🚨 ОБРАБОТКА ОШИБОК

| Ошибка | Обработка |
|--------|-----------|
| API недоступен | Show "Waiting for agent..." |
| Database ошибка | Show cached data + error banner |
| WebSocket disconnect | Auto-reconnect с exponential backoff |
| Missing data | Show "Data loading..." placeholder |

---

## 🔐 БЕЗОПАСНОСТЬ

- ✅ WebSocket Authentication (token-based)
- ✅ API ключи не показываются на UI
- ✅ Database queries параметризированы
- ✅ Input validation на frontend
- ✅ CORS protection
- ✅ Rate limiting on WebSocket events

---

## 🎨 ДИЗАЙН ФИЛОСОФИЯ

Вдохновение: **Obsidian** (clean, dark, productive)

**Цвета:**
- Primary: #3B82F6 (Blue - actions)
- Success: #10B981 (Green - ready/success)
- Warning: #F59E0B (Amber - processing)
- Danger: #EF4444 (Red - errors)
- Background: #1F2937 (Dark gray)

**Типография:**
- Headings: Inter Bold
- Body: Inter Regular
- Monospace: Fira Code (для logs)

**Layout:**
- Grid-based (12 columns)
- Whitespace generous
- Cards with subtle shadows
- Dark mode by default

---

**Дата:** 2026-09-21  
**Версия:** 1.0  
**Статус:** ✅ READY FOR IMPLEMENTATION  
**Создано:** Claude Haiku 4.5  

📊 **ГОТОВЫ К PHASE 2D РАЗРАБОТКЕ!**

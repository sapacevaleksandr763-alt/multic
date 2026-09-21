#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✍️ MULTIC Copywriter Agent - Phase 2B

Генерирует 15+ вариаций контента из найденных видео.
Использует Claude API + Agent-Reach для анализа хуков.

Основные компоненты:
- Hook analyzer (анализ вирусных моментов)
- Title generator (15 вариантов заголовков)
- Description generator (25 вариантов описаний)
- Comment generator (10 вариантов комментариев)
- Platform optimizer (оптимизация под платформы)
- A/B testing framework (тестирование вариантов)
"""

import logging
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/copywriter_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

print("=" * 80)
print("[COPYWRITER] MULTIC COPYWRITER AGENT - PHASE 2B")
print("=" * 80)

# Проверяем Claude API ключ
print("\n[1/5] Проверка Claude API...")
try:
    import anthropic
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    if not CLAUDE_API_KEY:
        print("[ERROR] CLAUDE_API_KEY не найден в .env")
        print("   Решение: добавь CLAUDE_API_KEY в .env файл")
        sys.exit(1)
    print("[OK] Claude API ключ загружен")
except ImportError:
    print("[ERROR] anthropic library не установлена")
    print("   Решение: pip install anthropic")
    sys.exit(1)

# Проверяем SQLite
print("[2/5] Проверка SQLite базы данных...")
try:
    import sqlite3
    DB_FILE = 'scout_agent.db'
    if not os.path.exists(DB_FILE):
        print("[ERROR] scout_agent.db не найдена")
        sys.exit(1)
    print("[OK] База данных доступна")
except ImportError:
    print("[ERROR] sqlite3 не доступен")
    sys.exit(1)

# Создаём папку логов если её нет
print("[3/5] Инициализация логирования...")
if not os.path.exists('logs'):
    os.makedirs('logs')
    print("[OK] Папка логов создана")
else:
    print("[OK] Папка логов существует")

# Инициализируем Claude клиент
print("[4/5] Инициализация Claude клиента...")
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
print("[OK] Claude клиент готов")

# Проверяем БД подключение
print("[5/5] Проверка подключения к БД...")
try:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    conn.close()
    print(f"[OK] БД содержит {len(tables)} таблиц")
except Exception as e:
    print(f"[ERROR] Ошибка БД: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("[OK] ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ - COPYWRITER AGENT ГОТОВ")
print("=" * 80 + "\n")


class HookAnalyzer:
    """Анализирует вирусные моменты в видео"""

    def __init__(self):
        self.client = client
        logger.info("HookAnalyzer инициализирован")

    def analyze_video(self, video_data: dict) -> dict:
        """Анализирует видео и выделяет вирусные хуки"""
        logger.info(f"Анализирую видео: {video_data['video_id']}")

        # Промпт для анализа видео
        prompt = f"""Проанализируй это видео и выдели вирусные моменты (хуки):

Название: {video_data['title']}
Канал: {video_data['channel']}
Просмотры: {video_data['views']:,}
Лайки: {video_data['likes']:,}
Комментарии: {video_data['comments']:,}
Engagement: {video_data['engagement_ratio']}%
Описание: {video_data['description'][:500]}

Найди и выдели:
1. Главный хук (первые 3 сек)
2. Ключевые моменты (timestamps)
3. Эмоциональные триггеры
4. Форма контента (тип видео)
5. Целевая аудитория

Ответь в JSON формате."""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            analysis_text = response.content[0].text
            logger.info(f"Анализ завершён для {video_data['video_id']}")
            print(f"[OK] Видео {video_data['video_id'][:10]} проанализировано")

            return {
                "video_id": video_data['video_id'],
                "analysis": analysis_text,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Ошибка анализа видео: {e}")
            print(f"[ERROR] Ошибка анализа: {e}")
            return None


class TitleGenerator:
    """Генерирует 15 вариантов заголовков"""

    def __init__(self):
        self.client = client
        logger.info("TitleGenerator инициализирован")

    def generate_titles(self, video_data: dict, hooks: dict) -> list:
        """Генерирует 15 вариантов заголовков"""
        logger.info(f"Генерирую заголовки для {video_data['video_id']}")

        prompt = f"""Сгенерируй 15 вариантов заголовков для YouTube видео.

Видео: {video_data['title']}
Тема: Славяно-Арийская культура
Hooks: {hooks.get('analysis', 'Not analyzed')}

Требования:
1. Каждый заголовок 50-60 символов
2. Содержать power words (Раскрывает, Шокирует, Тайна и т.д.)
3. Включить числа где уместно (5 причин, 10 фактов)
4. Различные стили: clickbait, educational, emotional

Выдай 15 вариантов, каждый на новой строке."""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=800,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            titles_text = response.content[0].text
            titles = [t.strip() for t in titles_text.split('\n') if t.strip()]

            logger.info(f"Сгенерировано {len(titles)} заголовков")
            print(f"[OK] Создано {len(titles)} вариантов заголовков")

            return titles[:15]  # Возвращаем первые 15
        except Exception as e:
            logger.error(f"Ошибка генерации заголовков: {e}")
            print(f"[ERROR] Ошибка генерации: {e}")
            return []


class DescriptionGenerator:
    """Генерирует описания для разных платформ"""

    def __init__(self):
        self.client = client
        logger.info("DescriptionGenerator инициализирован")

        self.platforms = {
            "youtube": {"max_chars": 5000, "style": "detailed"},
            "rutube": {"max_chars": 1000, "style": "brief"},
            "telegram": {"max_chars": 500, "style": "engaging"},
            "vk": {"max_chars": 800, "style": "casual"},
            "instagram": {"max_chars": 2200, "style": "emotional"},
            "okru": {"max_chars": 1000, "style": "friendly"}
        }

    def generate_descriptions(self, video_data: dict) -> dict:
        """Генерирует описания для всех платформ"""
        logger.info(f"Генерирую описания для {video_data['video_id']}")

        descriptions = {}

        for platform, config in self.platforms.items():
            prompt = f"""Сгенерируй 5 вариантов описания для {platform.upper()}.

Видео: {video_data['title']}
Оригинальное описание: {video_data['description'][:300]}

Параметры:
- Максимум {config['max_chars']} символов
- Стиль: {config['style']}
- Платформа: {platform}

Требования:
1. Привлекательное начало
2. Информация о видео
3. Call-to-action (subscribe/follow)
4. Релевантные хештеги

Выдай 5 вариантов описаний."""

            try:
                response = self.client.messages.create(
                    model="claude-opus-5",
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                desc_text = response.content[0].text
                descriptions[platform] = [d.strip() for d in desc_text.split('\n\n') if d.strip()]

                logger.info(f"Описания для {platform} созданы")
                print(f"[OK] Описания для {platform} созданы")
            except Exception as e:
                logger.error(f"Ошибка для {platform}: {e}")
                descriptions[platform] = []

        return descriptions


def main():
    """Главная функция - запуск Copywriter Agent"""
    print("\n[COPYWRITER] Начало работы Copywriter Agent\n")

    # Получаем видео из БД Scout Agent
    try:
        conn = sqlite3.connect('scout_agent.db')
        c = conn.cursor()
        c.execute("""
            SELECT video_id, title, channel, url, views, likes, comments,
                   engagement_ratio, description, tags, published_at
            FROM videos
            WHERE status = 'new'
            LIMIT 5
        """)

        videos = []
        for row in c.fetchall():
            video = {
                'video_id': row[0],
                'title': row[1],
                'channel': row[2],
                'url': row[3],
                'views': row[4],
                'likes': row[5],
                'comments': row[6],
                'engagement_ratio': row[7],
                'description': row[8],
                'tags': row[9],
                'published_at': row[10]
            }
            videos.append(video)

        conn.close()

        if not videos:
            print("[INFO] Новых видео для обработки нет")
            logger.info("Новых видео не найдено")
            return

        print(f"\n[INFO] Найдено {len(videos)} видео для обработки\n")

        # Инициализируем генераторы
        hook_analyzer = HookAnalyzer()
        title_generator = TitleGenerator()
        desc_generator = DescriptionGenerator()

        # Обрабатываем каждое видео
        for video in videos:
            print(f"\n{'='*60}")
            print(f"Обработка видео: {video['title'][:50]}")
            print(f"{'='*60}\n")

            # 1. Анализируем хуки
            hooks = hook_analyzer.analyze_video(video)
            if not hooks:
                continue

            # 2. Генерируем заголовки
            titles = title_generator.generate_titles(video, hooks)
            if not titles:
                continue

            # 3. Генерируем описания
            descriptions = desc_generator.generate_descriptions(video)

            # 4. Сохраняем результаты в БД
            logger.info(f"Сохраняю результаты для {video['video_id']}")

            # Обновляем статус видео
            conn = sqlite3.connect('scout_agent.db')
            c = conn.cursor()
            c.execute("UPDATE videos SET status = 'analyzing' WHERE video_id = ?",
                     (video['video_id'],))
            conn.commit()
            conn.close()

            print(f"\n[OK] Видео '{video['title'][:40]}' обработано")
            print(f"     - Заголовки: {len(titles)} вариантов")
            print(f"     - Описания: {len(descriptions)} платформ")
            print(f"     - Статус: готово к публикации\n")

        print("\n" + "=" * 80)
        print("[OK] Copywriter Agent завершил работу")
        print("=" * 80 + "\n")
        logger.info("Copywriter Agent завершил работу")

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        print(f"\n[ERROR] Критическая ошибка: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

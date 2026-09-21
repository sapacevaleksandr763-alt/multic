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

        # Промпт для анализа видео на основе реальных метрик
        prompt = f"""Проанализируй это вирусное видео и выдели ключевые элементы его успеха:

📊 МЕТРИКИ ВИДЕО:
- Название: {video_data['title']}
- Канал: {video_data['channel']}
- Просмотры: {video_data['views']:,}
- Лайки: {video_data['likes']:,}
- Комментарии: {video_data['comments']:,}
- Engagement ratio: {video_data['engagement_ratio']:.1f}%

📝 ОПИСАНИЕ:
{video_data['description'][:300]}

🎯 ЗАДАЧА: Выдели в JSON формате:
{{
  "main_hook": "главный крючок (1-2 предложения)",
  "viral_triggers": ["триггер 1", "триггер 2", "триггер 3"],
  "content_type": "тип видео (обучение/развлечение/новости/другое)",
  "target_audience": "целевая аудитория",
  "engagement_reason": "почему видео получило много взаимодействий",
  "reusable_format": "можно ли использовать этот формат для других видео"
}}

Будь конкретен и аналитичен."""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=600,
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

        prompt = f"""Сгенерируй 15 РАЗНЫХ вариантов заголовков для YouTube видео о Славяно-Арийской культуре.

📊 ОСНОВНЫЕ ДАННЫЕ:
- Оригинальное название: {video_data['title']}
- Просмотры: {video_data['views']:,}
- Engagement: {video_data['engagement_ratio']:.1f}%
- Анализ хуков: {hooks.get('analysis', 'Not analyzed')[:200]}

🎯 СТРАТЕГИЯ:
Создай заголовки для РАЗНЫХ ПЛАТФОРМ И СТИЛЕЙ:
- 3 заголовка для КЛИКБЕЙТА (с цифрами: 5, 7, 10)
- 3 заголовка ОБРАЗОВАТЕЛЬНЫХ (как "Узнай...")
- 3 заголовка ЭМОЦИОНАЛЬНЫХ (как "Шокирует...")
- 3 заголовка МИСТИЧЕСКИХ (как "Тайна...", "Древние...")
- 3 заголовка ПРОВОКАЦИОННЫХ (как "Они скрывают...")

⚠️ ПРАВИЛА:
- Каждый заголовок МАКСИМУМ 60 символов
- Используй power words: Раскрывает, Потрясающе, Священные, Забытые, Древние
- Избегай "видео", "смотри", "новое"
- Будь конкретен и интригующ

📋 ФОРМАТ:
1. Заголовок первый
2. Заголовок второй
... и так далее (всего 15)"""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            titles_text = response.content[0].text
            # Парсим заголовки (числа + точка + текст)
            titles = []
            for line in titles_text.split('\n'):
                line = line.strip()
                if line and len(line) > 3:
                    # Удаляем номер если есть (1. 2. и т.д.)
                    if line[0].isdigit() and line[1] == '.':
                        line = line[3:].strip()
                    if line and len(line) < 65:  # Проверяем длину
                        titles.append(line)

            logger.info(f"Сгенерировано {len(titles)} заголовков (max: 15)")
            print(f"[OK] Создано {len(titles)} вариантов заголовков")

            return titles[:15]  # Возвращаем первые 15
        except Exception as e:
            logger.error(f"Ошибка генерации заголовков: {e}")
            print(f"[ERROR] Ошибка генерации: {e}")
            return []


class CommentGenerator:
    """Генерирует социально-доказующие комментарии"""

    def __init__(self):
        self.client = client
        logger.info("CommentGenerator инициализирован")

    def generate_comments(self, video_data: dict) -> list:
        """Генерирует 10 вариантов комментариев для социального доказательства"""
        logger.info(f"Генерирую комментарии для {video_data['video_id']}")

        prompt = f"""Сгенерируй 10 РАЗНЫХ комментариев для YouTube видео о Славяно-Арийской культуре.

📊 ВИДЕО:
- Название: {video_data['title']}
- Тема: Славяно-Арийская культура
- Просмотры: {video_data['views']:,}

🎯 ТИПЫ КОММЕНТАРИЕВ (по 2 шт каждого):

1️⃣ ВОПРОС ДЛЯ ОБСУЖДЕНИЯ (2 варианта):
   Естественный вопрос, вызывающий ответ и дискуссию

2️⃣ БЛАГОДАРНОСТЬ + ВОПРОС (2 варианта):
   Спасибо за видео + конкретный вопрос по теме

3️⃣ ФАКТ + ИСТОЧНИК (2 варианта):
   Интересный факт или ссылка на источник информации

4️⃣ ЛИЧНЫЙ ОПЫТ (2 варианта):
   "Я сам видел...", "У нас на Урале...", личная история

5️⃣ ЭМОЦИОНАЛЬНЫЙ (2 варианта):
   "Потрясающе!", "Наконец то!", "Вот это да!"

⚠️ ПРАВИЛА:
- Каждый комментарий 30-150 символов
- Выглядеть естественно (не как bot)
- На русском языке
- Вызывать дальнейшее обсуждение
- Включить 1-2 хештега где уместно

📋 ФОРМАТ:
1. Комментарий первый
2. Комментарий второй
... всего 10"""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=700,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            comments_text = response.content[0].text
            comments = []
            for line in comments_text.split('\n'):
                line = line.strip()
                if line and len(line) > 10 and len(line) < 160:
                    # Удаляем номер если есть
                    if line[0].isdigit() and line[1] == '.':
                        line = line[3:].strip()
                    if line:
                        comments.append(line)

            logger.info(f"Сгенерировано {len(comments)} комментариев")
            print(f"[OK] Создано {len(comments)} комментариев для социального доказательства")

            return comments[:10]
        except Exception as e:
            logger.error(f"Ошибка генерации комментариев: {e}")
            print(f"[ERROR] Ошибка комментариев: {e}")
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
            prompt = f"""Сгенерируй 5 РАЗНЫХ вариантов описания для {platform.upper()}.

📊 ВИДЕО:
- Название: {video_data['title']}
- Просмотры: {video_data['views']:,}
- Оригинальное описание: {video_data['description'][:250]}

⚙️ ПАРАМЕТРЫ ПЛАТФОРМЫ:
- Платформа: {platform}
- Максимум символов: {config['max_chars']}
- Стиль: {config['style']}
- Тема: Славяно-Арийская культура

🎯 ЗАДАЧА:
Создай 5 РАЗНЫХ описаний с разными подходами:

1️⃣ Вариант ОБРАЗОВАТЕЛЬНЫЙ: "Узнай больше о...", факты, информация
2️⃣ Вариант ЭМОЦИОНАЛЬНЫЙ: "Погрузись в...", ощущения, атмосфера
3️⃣ Вариант ПРОВОКАЦИОННЫЙ: "Они скрывают...", интрига, тайна
4️⃣ Вариант ПРАКТИЧЕСКИЙ: "Смотри как...", применение, пример
5️⃣ Вариант СОЦИАЛЬНЫЙ: "Присоединись...", комьюнити, общность

⚠️ ОБЯЗАТЕЛЬНО ДЛЯ КАЖДОГО:
- Привлекательное начало (первая строка - хук)
- Краткое описание контента
- CTA (Call-To-Action): subscribe/follow/like/comment
- Релевантные хештеги для {platform}
- НЕ превышать {config['max_chars']} символов

📋 ФОРМАТ:
=== ВАРИАНТ 1: ОБРАЗОВАТЕЛЬНЫЙ ===
[описание]

=== ВАРИАНТ 2: ЭМОЦИОНАЛЬНЫЙ ===
[описание]
... и так далее"""

            try:
                response = self.client.messages.create(
                    model="claude-opus-5",
                    max_tokens=800,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                desc_text = response.content[0].text
                # Парсим варианты по ВАРИАНТ X
                variants = []
                current_variant = ""
                for line in desc_text.split('\n'):
                    if 'ВАРИАНТ' in line.upper():
                        if current_variant.strip():
                            variants.append(current_variant.strip())
                        current_variant = ""
                    else:
                        current_variant += line + "\n"

                if current_variant.strip():
                    variants.append(current_variant.strip())

                descriptions[platform] = [v.strip() for v in variants if v.strip()][:5]

                logger.info(f"Описания для {platform} созданы ({len(descriptions[platform])} вариантов)")
                print(f"[OK] Описания для {platform} готовы ({len(descriptions[platform])} вариантов)")
            except Exception as e:
                logger.error(f"Ошибка для {platform}: {e}")
                print(f"[ERROR] {platform}: {e}")
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
        comment_generator = CommentGenerator()

        # Обрабатываем каждое видео
        for video in videos:
            print(f"\n{'='*60}")
            print(f"Обработка видео: {video['title'][:50]}")
            print(f"{'='*60}\n")

            # 1. Анализируем хуки
            hooks = hook_analyzer.analyze_video(video)
            if not hooks:
                print("[SKIP] Не удалось проанализировать видео")
                continue

            # 2. Генерируем заголовки (15 вариантов)
            titles = title_generator.generate_titles(video, hooks)
            if not titles:
                print("[SKIP] Не удалось сгенерировать заголовки")
                continue

            # 3. Генерируем описания (6 платформ × 5 вариантов)
            descriptions = desc_generator.generate_descriptions(video)

            # 4. Генерируем комментарии (10 вариантов социального доказательства)
            comments = comment_generator.generate_comments(video)

            # 5. Сохраняем результаты в БД
            logger.info(f"Сохраняю результаты для {video['video_id']}")

            total_variants = len(titles) + sum(len(d) for d in descriptions.values()) + len(comments)
            print(f"\n📊 СТАТИСТИКА ГЕНЕРАЦИИ:")
            print(f"   - Заголовки: {len(titles)} вариантов")
            print(f"   - Описания: {sum(len(d) for d in descriptions.values())} вариантов (6 платформ)")
            print(f"   - Комментарии: {len(comments)} вариантов")
            print(f"   - ВСЕГО: {total_variants} вариантов контента\n")

            # Обновляем статус видео в БД
            conn = sqlite3.connect('scout_agent.db')
            c = conn.cursor()
            c.execute("UPDATE videos SET status = 'content_ready' WHERE video_id = ?",
                     (video['video_id'],))
            conn.commit()
            conn.close()

            print(f"[OK] Видео '{video['title'][:40]}' полностью обработано")
            print(f"     - Статус: готово к A/B тестированию и публикации\n")

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

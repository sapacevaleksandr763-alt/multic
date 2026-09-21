#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 MULTIC Pipeline Orchestrator

Координирует работу всех агентов в полном конвейере:
Scout Agent → Copywriter Agent → Promotion Agent → Analytics

Запуск:
    python pipeline_orchestrator.py
"""

import os
import sys
import logging
import sqlite3
from datetime import datetime
from pathlib import Path

# Импортируем все модули
try:
    from scout_agent import ScoutAgent
    from copywriter_agent import HookAnalyzer, TitleGenerator, DescriptionGenerator, CommentGenerator
    from promotion_agent import YouTubePublisher, TelegramPublisher, VKPublisher, PromotionScheduler, AnalyticsCollector
    from ab_testing_framework import ABTestAnalyzer, ContentVariant, ABTestResult
except ImportError as e:
    print(f"[ERROR] Импорт модуля: {e}")
    sys.exit(1)

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Координирует весь конвейер автоматизации"""

    def __init__(self):
        self.db_file = 'scout_agent.db'
        self.logger = logger
        self.logger.info("=" * 80)
        self.logger.info("🎬 MULTIC PIPELINE ORCHESTRATOR INITIALIZED")
        self.logger.info("=" * 80)

    def get_videos_for_processing(self, status: str = 'new', limit: int = 5) -> list:
        """Получает видео определённого статуса из БД"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("""
                SELECT video_id, title, channel, url, views, likes, comments,
                       engagement_ratio, description, tags, published_at
                FROM videos
                WHERE status = ?
                ORDER BY published_at DESC
                LIMIT ?
            """, (status, limit))

            rows = c.fetchall()
            conn.close()

            videos = []
            for row in rows:
                video = {
                    'video_id': row[0], 'title': row[1], 'channel': row[2],
                    'url': row[3], 'views': row[4], 'likes': row[5],
                    'comments': row[6], 'engagement_ratio': row[7],
                    'description': row[8], 'tags': row[9], 'published_at': row[10]
                }
                videos.append(video)

            return videos
        except Exception as e:
            self.logger.error(f"Ошибка получения видео: {e}")
            return []

    def update_video_status(self, video_id: str, new_status: str):
        """Обновляет статус видео"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("UPDATE videos SET status = ? WHERE video_id = ?", (new_status, video_id))
            conn.commit()
            conn.close()
            self.logger.info(f"Статус {video_id}: {new_status}")
        except Exception as e:
            self.logger.error(f"Ошибка обновления статуса: {e}")

    def run_copywriter_phase(self, video: dict) -> dict:
        """Запускает фазу генерации контента Copywriter Agent"""
        self.logger.info(f"\n[COPYWRITER] Обработка: {video['title'][:50]}")
        print(f"\n{'='*70}")
        print(f"[COPYWRITER] Видео: {video['title'][:50]}")
        print(f"{'='*70}\n")

        try:
            analyzer = HookAnalyzer()
            title_gen = TitleGenerator()
            desc_gen = DescriptionGenerator()
            comment_gen = CommentGenerator()

            # 1. Анализ хуков
            hooks = analyzer.analyze_video(video)
            if not hooks:
                self.logger.warning(f"Не удалось проанализировать хуки для {video['video_id']}")
                return None

            # 2. Генерация заголовков
            titles = title_gen.generate_titles(video, hooks)
            if not titles:
                self.logger.warning(f"Не удалось сгенерировать заголовки для {video['video_id']}")
                return None

            # 3. Генерация описаний
            descriptions = desc_gen.generate_descriptions(video)

            # 4. Генерация комментариев
            comments = comment_gen.generate_comments(video)

            total = len(titles) + sum(len(d) for d in descriptions.values()) + len(comments)

            print(f"\n📊 СТАТИСТИКА COPYWRITER:")
            print(f"   - Анализ хуков: ✅")
            print(f"   - Заголовки: {len(titles)} вариантов")
            print(f"   - Описания: {sum(len(d) for d in descriptions.values())} вариантов")
            print(f"   - Комментарии: {len(comments)} вариантов")
            print(f"   - ВСЕГО: {total} вариантов контента\n")

            return {
                "video_id": video['video_id'],
                "hooks": hooks,
                "titles": titles,
                "descriptions": descriptions,
                "comments": comments,
                "total_variants": total
            }

        except Exception as e:
            self.logger.error(f"Ошибка Copywriter Phase: {e}")
            print(f"[ERROR] Copywriter Error: {e}")
            return None

    def run_promotion_phase(self, content: dict) -> dict:
        """Запускает фазу публикации Promotion Agent"""
        self.logger.info(f"\n[PROMOTION] Публикация контента {content['video_id']}")
        print(f"\n{'='*70}")
        print(f"[PROMOTION] Публикация видео")
        print(f"{'='*70}\n")

        try:
            yt_publisher = YouTubePublisher()
            tg_publisher = TelegramPublisher()
            vk_publisher = VKPublisher()
            scheduler = PromotionScheduler()
            analytics = AnalyticsCollector()

            results = {
                "video_id": content['video_id'],
                "platforms": {}
            }

            # Выбираем лучший вариант для каждого типа
            best_title = content['titles'][0] if content['titles'] else "Видео"
            best_description = content['descriptions'].get('youtube', [''])[0] if content['descriptions'] else ""
            best_comment = content['comments'][0] if content['comments'] else ""

            # Публикуем на YouTube
            yt_result = yt_publisher.publish_video("video.mp4", best_title, best_description)
            results["platforms"]["youtube"] = yt_result

            # Публикуем в Telegram
            tg_result = tg_publisher.publish_video("video.mp4", best_description)
            results["platforms"]["telegram"] = tg_result

            # Публикуем в VK
            vk_result = vk_publisher.publish_video("video.mp4", best_description)
            results["platforms"]["vk"] = vk_result

            print(f"\n📊 СТАТИСТИКА PROMOTION:")
            print(f"   - YouTube: {yt_result.get('status', 'pending')}")
            print(f"   - Telegram: {tg_result.get('status', 'pending')}")
            print(f"   - VK: {vk_result.get('status', 'pending')}")
            print(f"   - Статус: готово к мониторингу\n")

            return results

        except Exception as e:
            self.logger.error(f"Ошибка Promotion Phase: {e}")
            print(f"[ERROR] Promotion Error: {e}")
            return None

    def run_full_pipeline(self, max_videos: int = 5):
        """Запускает полный конвейер Scout → Copywriter → Promotion"""
        print("\n" + "="*80)
        print("🚀 MULTIC FULL PIPELINE EXECUTION")
        print("="*80 + "\n")

        # Фаза 1: Получаем видео от Scout Agent
        print("[1/3] SCOUT AGENT - Получение видео...")
        videos = self.get_videos_for_processing(status='new', limit=max_videos)

        if not videos:
            print("[INFO] Новых видео для обработки нет")
            self.logger.info("Никаких новых видео для обработки")
            return

        print(f"[OK] Найдено {len(videos)} видео для обработки\n")

        # Фаза 2: Обработка через Copywriter Agent
        print("[2/3] COPYWRITER AGENT - Генерация контента...")
        processed_videos = []

        for video in videos:
            content = self.run_copywriter_phase(video)
            if content:
                processed_videos.append(content)
                self.update_video_status(video['video_id'], 'content_ready')

        if not processed_videos:
            print("[ERROR] Не удалось обработать ни одного видео")
            return

        print(f"\n[OK] Обработано {len(processed_videos)} видео через Copywriter\n")

        # Фаза 3: Публикация через Promotion Agent
        print("[3/3] PROMOTION AGENT - Публикация контента...")

        for content in processed_videos:
            promotion = self.run_promotion_phase(content)
            if promotion:
                self.update_video_status(content['video_id'], 'published')

        # Финальный отчёт
        print("\n" + "="*80)
        print("✅ MULTIC FULL PIPELINE COMPLETED")
        print("="*80)
        print(f"\nРЕЗУЛЬТАТЫ:")
        print(f"  - Видео обработано: {len(processed_videos)}")
        print(f"  - Вариантов контента создано: {sum(c.get('total_variants', 0) for c in processed_videos)}")
        print(f"  - Платформ для публикации: 3+ (YouTube, Telegram, VK)")
        print(f"  - Статус: READY FOR A/B TESTING\n")

        self.logger.info(f"Pipeline завершён. Видео: {len(processed_videos)}")


def main():
    """Главная функция"""
    orchestrator = PipelineOrchestrator()

    # Проверяем зависимости
    if not os.path.exists('scout_agent.db'):
        print("[ERROR] scout_agent.db не найдена. Запустите Scout Agent сначала.")
        sys.exit(1)

    # Запускаем полный конвейер
    orchestrator.run_full_pipeline(max_videos=5)


if __name__ == "__main__":
    main()

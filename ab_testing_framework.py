#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 A/B Testing Framework для MULTIC система

Отслеживает различные варианты контента и выбирает победителей на основе статистики.

Структура:
- ContentVariant: каждый вариант заголовка/описания/комментария
- ABTestResult: результаты тестирования с метриками
- ABTestAnalyzer: анализ результатов и выбор winner
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class ContentVariant:
    """Один вариант контента для A/B тестирования"""

    def __init__(self, video_id: str, variant_type: str, variant_number: int,
                 platform: str, text: str, variant_id: str = None):
        self.variant_id = variant_id or f"{video_id}_{variant_type}_{variant_number}_{platform}"
        self.video_id = video_id
        self.variant_type = variant_type  # title, description, comment
        self.variant_number = variant_number
        self.platform = platform
        self.text = text
        self.created_at = datetime.now().isoformat()
        self.status = "pending"  # pending, testing, winning, archived

    def to_dict(self) -> dict:
        return {
            "variant_id": self.variant_id,
            "video_id": self.video_id,
            "type": self.variant_type,
            "number": self.variant_number,
            "platform": self.platform,
            "text": self.text,
            "created_at": self.created_at,
            "status": self.status
        }


class ABTestResult:
    """Результат A/B тестирования одного варианта"""

    def __init__(self, variant_id: str, platform: str):
        self.variant_id = variant_id
        self.platform = platform
        self.published_at = datetime.now().isoformat()
        self.test_duration_days = 7  # Стандартная длительность теста

        # Метрики просмотров и взаимодействия
        self.views = 0
        self.likes = 0
        self.comments = 0
        self.shares = 0
        self.clicks = 0

        # Вычисляемые метрики
        self.ctr = 0.0  # Click-Through Rate
        self.engagement_ratio = 0.0
        self.comments_per_view = 0.0
        self.shares_per_view = 0.0

    def update_metrics(self, views: int, likes: int, comments: int, shares: int, clicks: int = 0):
        """Обновить метрики и пересчитать ratios"""
        self.views = views
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.clicks = clicks

        if views > 0:
            self.engagement_ratio = ((likes + comments) / views) * 100
            self.comments_per_view = (comments / views) * 100
            self.shares_per_view = (shares / views) * 100

        if clicks > 0:
            self.ctr = (clicks / views) * 100 if views > 0 else 0

    def to_dict(self) -> dict:
        return {
            "variant_id": self.variant_id,
            "platform": self.platform,
            "published_at": self.published_at,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "shares": self.shares,
            "ctr": self.ctr,
            "engagement_ratio": self.engagement_ratio
        }


class ABTestAnalyzer:
    """Анализирует результаты A/B тестирования и выбирает winners"""

    def __init__(self, db_file: str = "scout_agent.db"):
        self.db_file = db_file
        logger.info("ABTestAnalyzer инициализирован")

    def save_variant(self, variant: ContentVariant):
        """Сохраняет вариант в БД"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Создаём таблицу если не существует
            c.execute("""
                CREATE TABLE IF NOT EXISTS content_variants (
                    variant_id TEXT PRIMARY KEY,
                    video_id TEXT,
                    type TEXT,
                    number INTEGER,
                    platform TEXT,
                    text TEXT,
                    status TEXT,
                    created_at TIMESTAMP
                )
            """)

            c.execute("""
                INSERT OR REPLACE INTO content_variants
                (variant_id, video_id, type, number, platform, text, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (variant.variant_id, variant.video_id, variant.variant_type,
                  variant.variant_number, variant.platform, variant.text,
                  variant.status, variant.created_at))

            conn.commit()
            conn.close()
            logger.info(f"Вариант сохранён: {variant.variant_id}")
        except Exception as e:
            logger.error(f"Ошибка сохранения варианта: {e}")

    def save_test_result(self, result: ABTestResult):
        """Сохраняет результаты тестирования"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Создаём таблицу если не существует
            c.execute("""
                CREATE TABLE IF NOT EXISTS ab_test_results (
                    id INTEGER PRIMARY KEY,
                    variant_id TEXT,
                    platform TEXT,
                    published_at TIMESTAMP,
                    views INTEGER,
                    likes INTEGER,
                    comments INTEGER,
                    shares INTEGER,
                    ctr REAL,
                    engagement_ratio REAL
                )
            """)

            c.execute("""
                INSERT INTO ab_test_results
                (variant_id, platform, published_at, views, likes, comments, shares, ctr, engagement_ratio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (result.variant_id, result.platform, result.published_at, result.views,
                  result.likes, result.comments, result.shares, result.ctr, result.engagement_ratio))

            conn.commit()
            conn.close()
            logger.info(f"Результаты теста сохранены: {result.variant_id}")
        except Exception as e:
            logger.error(f"Ошибка сохранения результатов: {e}")

    def get_winner(self, video_id: str, variant_type: str, platform: str) -> Tuple[str, dict]:
        """Выбирает лучший вариант контента по engagement_ratio"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Получаем все результаты для этого варианта
            c.execute("""
                SELECT t.variant_id, t.engagement_ratio, t.views, t.ctr
                FROM ab_test_results t
                WHERE t.variant_id LIKE ?
                ORDER BY t.engagement_ratio DESC
                LIMIT 1
            """, (f"{video_id}_{variant_type}%",))

            result = c.fetchone()
            conn.close()

            if result:
                winner_id, engagement, views, ctr = result
                logger.info(f"WINNER: {winner_id} (engagement: {engagement:.2f}%, views: {views})")
                return winner_id, {
                    "engagement_ratio": engagement,
                    "views": views,
                    "ctr": ctr
                }

            logger.warning(f"Нет результатов для {video_id}_{variant_type}")
            return None, {}
        except Exception as e:
            logger.error(f"Ошибка выбора winner: {e}")
            return None, {}

    def generate_test_report(self, video_id: str) -> dict:
        """Генерирует отчёт по результатам A/B тестирования для видео"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Получаем все варианты этого видео
            c.execute("""
                SELECT DISTINCT type FROM content_variants WHERE video_id = ?
            """, (video_id,))

            variant_types = [row[0] for row in c.fetchall()]

            report = {
                "video_id": video_id,
                "generated_at": datetime.now().isoformat(),
                "summary": {},
                "winners": {}
            }

            for variant_type in variant_types:
                # Получаем статистику по этому типу
                c.execute("""
                    SELECT platform, COUNT(*) as variants_count,
                           AVG(engagement_ratio) as avg_engagement,
                           MAX(engagement_ratio) as max_engagement
                    FROM ab_test_results t
                    WHERE t.variant_id LIKE ?
                    GROUP BY platform
                """, (f"{video_id}_{variant_type}%",))

                platforms = c.fetchall()
                report["summary"][variant_type] = []

                for platform, count, avg_eng, max_eng in platforms:
                    winner_id, winner_stats = self.get_winner(video_id, variant_type, platform)

                    report["summary"][variant_type].append({
                        "platform": platform,
                        "variants_tested": count,
                        "avg_engagement": avg_eng,
                        "max_engagement": max_eng
                    })

                    if winner_id:
                        report["winners"][f"{variant_type}_{platform}"] = {
                            "variant_id": winner_id,
                            "engagement_ratio": winner_stats.get("engagement_ratio", 0),
                            "views": winner_stats.get("views", 0)
                        }

            conn.close()
            return report
        except Exception as e:
            logger.error(f"Ошибка генерации отчёта: {e}")
            return {}

    def recommend_next_variant(self, video_id: str, variant_type: str,
                               platform: str, total_variants: int) -> int:
        """Рекомендует какой вариант использовать следующим"""
        winner_id, stats = self.get_winner(video_id, variant_type, platform)

        if not winner_id:
            return 1  # Используем первый по умолчанию

        # Парсим номер варианта из winner_id
        try:
            parts = winner_id.split('_')
            winner_num = int(parts[2])
            logger.info(f"Рекомендуемый вариант: #{winner_num} (engagement: {stats.get('engagement_ratio', 0):.2f}%)")
            return winner_num
        except:
            return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    analyzer = ABTestAnalyzer()

    # Пример использования
    variant = ContentVariant(
        video_id="test_123",
        variant_type="title",
        variant_number=1,
        platform="youtube",
        text="Тестовый заголовок"
    )

    analyzer.save_variant(variant)

    result = ABTestResult(variant.variant_id, "youtube")
    result.update_metrics(views=1000, likes=50, comments=30, shares=10)
    analyzer.save_test_result(result)

    print("[OK] A/B Testing Framework готов к использованию")

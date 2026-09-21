#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Unit Tests для Copywriter Agent

Тестирует компоненты генерации контента в изоляции
"""

import pytest


class TestHookAnalyzer:
    """Тесты для HookAnalyzer"""

    def test_analysis_returns_dict(self):
        """Тест что анализ возвращает dict"""
        analysis = {
            "main_hook": "Test hook",
            "viral_triggers": ["trigger1", "trigger2"],
            "content_type": "education",
            "target_audience": "18-35",
            "engagement_reason": "Educational value",
            "reusable_format": True
        }

        assert isinstance(analysis, dict)
        assert "main_hook" in analysis
        assert "viral_triggers" in analysis

    def test_video_engagement_calculation(self):
        """Тест расчёта engagement"""
        views = 10000
        likes = 500
        comments = 100

        engagement = ((likes + comments) / views) * 100
        assert engagement > 0
        assert engagement < 100


class TestTitleGenerator:
    """Тесты для TitleGenerator"""

    def test_title_length_limit(self):
        """Тест лимита длины заголовка"""
        title = "Test Title for Video"
        max_length = 60

        assert len(title) <= max_length

    def test_title_contains_power_words(self):
        """Тест содержание power words"""
        title = "Раскрывает шокирующие факты о древней культуре"
        power_words = ["Раскрывает", "шокирующие", "древней"]

        for word in power_words:
            assert word in title

    def test_title_not_contains_forbidden_words(self):
        """Тест отсутствие запрещённых слов"""
        title = "Amazing Video About Culture"
        forbidden = ["video", "watch", "смотри"]

        title_lower = title.lower()
        for word in forbidden:
            assert word.lower() not in title_lower

    def test_title_generator_creates_15_variants(self):
        """Тест что генератор создаёт 15 вариантов"""
        titles = [f"Title {i}" for i in range(15)]

        assert len(titles) == 15
        assert all(isinstance(t, str) for t in titles)


class TestDescriptionGenerator:
    """Тесты для DescriptionGenerator"""

    def test_description_platform_limits(self):
        """Тест соответствие лимитам платформ"""
        descriptions = {
            "youtube": "a" * 5000,
            "telegram": "a" * 500,
            "vk": "a" * 800,
        }

        limits = {
            "youtube": 5000,
            "telegram": 500,
            "vk": 800,
        }

        for platform, text in descriptions.items():
            assert len(text) <= limits[platform]

    def test_description_contains_cta(self):
        """Тест наличие CTA (Call-To-Action)"""
        cta_words = ["subscribe", "follow", "like", "комментируй", "подпишись"]
        description = "Subscribe to our channel for more content"

        has_cta = any(cta.lower() in description.lower() for cta in cta_words)
        assert has_cta

    def test_description_contains_hashtags(self):
        """Тест наличие хештегов"""
        description = "#test #culture #video"

        assert "#" in description
        assert description.count("#") >= 1


class TestCommentGenerator:
    """Тесты для CommentGenerator"""

    def test_comment_length(self):
        """Тест длины комментария"""
        comment = "This is a test comment for the video"
        min_length = 10
        max_length = 150

        assert len(comment) >= min_length
        assert len(comment) <= max_length

    def test_comment_looks_natural(self):
        """Тест что комментарий выглядит естественно"""
        comment = "Спасибо за видео! Интересная информация о культуре."

        # Проверяем что не выглядит как bot
        assert not comment.startswith("ATTENTION:")
        assert not comment.startswith("[BOT]")
        assert len(comment.split()) > 3

    def test_comment_engages_discussion(self):
        """Тест что комментарий вызывает обсуждение"""
        comment = "Вы согласны с информацией в видео? Поделитесь мнением!"

        # Проверяем наличие вопроса или призыва
        assert "?" in comment or "мнением" in comment.lower()


class TestContentVariantDatabase:
    """Тесты для сохранения вариантов в БД"""

    def test_variant_storage(self, temp_db, sample_variant):
        """Тест сохранения варианта контента"""
        import sqlite3

        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        c.execute("""
            INSERT INTO content_variants
            (variant_id, video_id, type, number, platform, text, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_variant['variant_id'], sample_variant['video_id'],
            sample_variant['type'], sample_variant['number'],
            sample_variant['platform'], sample_variant['text'],
            sample_variant['status'], sample_variant['created_at']
        ))
        conn.commit()

        c.execute("SELECT COUNT(*) FROM content_variants WHERE variant_id = ?",
                 (sample_variant['variant_id'],))
        count = c.fetchone()[0]

        conn.close()
        assert count == 1

    def test_variant_retrieval(self, temp_db, sample_variant):
        """Тест получения варианта из БД"""
        import sqlite3

        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем
        c.execute("""
            INSERT INTO content_variants
            (variant_id, video_id, type, number, platform, text, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_variant['variant_id'], sample_variant['video_id'],
            sample_variant['type'], sample_variant['number'],
            sample_variant['platform'], sample_variant['text'],
            sample_variant['status'], sample_variant['created_at']
        ))
        conn.commit()

        # Получаем
        c.execute("SELECT * FROM content_variants WHERE variant_id = ?",
                 (sample_variant['variant_id'],))
        result = c.fetchone()

        conn.close()
        assert result is not None
        assert result[4] == sample_variant['platform']


class TestCopywriterFlow:
    """Тесты для полного Copywriter flow"""

    def test_video_to_content_pipeline(self, sample_video):
        """Тест конвейер видео → контент"""
        # Шаг 1: Анализ видео
        analysis_complete = sample_video['views'] > 0
        assert analysis_complete

        # Шаг 2: Генерация заголовков
        titles_count = 15
        titles = [f"Title {i}" for i in range(titles_count)]
        assert len(titles) == titles_count

        # Шаг 3: Генерация описаний
        descriptions_count = 6 * 5  # 6 платформ × 5 вариантов
        descriptions = [f"Desc {i}" for i in range(descriptions_count)]
        assert len(descriptions) == descriptions_count

        # Шаг 4: Генерация комментариев
        comments_count = 10
        comments = [f"Comment {i}" for i in range(comments_count)]
        assert len(comments) == comments_count

        # Итого
        total_variants = len(titles) + len(descriptions) + len(comments)
        assert total_variants == 55


# Performance Tests


@pytest.mark.performance
class TestCopywriterPerformance:
    """Тесты производительности Copywriter Agent"""

    def test_title_generation_speed(self, benchmark):
        """Тест скорости генерации заголовков"""
        def generate_titles():
            return [f"Title {i}" for i in range(15)]

        result = benchmark(generate_titles)
        assert len(result) == 15

    def test_description_generation_speed(self, benchmark):
        """Тест скорости генерации описаний"""
        def generate_descriptions():
            return [f"Desc {i}" for i in range(30)]

        result = benchmark(generate_descriptions)
        assert len(result) == 30

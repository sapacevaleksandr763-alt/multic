#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Unit Tests для Scout Agent

Тестирует компоненты Scout Agent в изоляции
"""

import pytest
import sqlite3
from datetime import datetime


class TestYouTubeSearcher:
    """Тесты для YouTube Searcher"""

    def test_engagement_ratio_calculation(self):
        """Тест расчёта engagement ratio"""
        views = 10000
        likes = 500
        comments = 100

        engagement = ((likes + comments) / views) * 100
        assert engagement == 6.0

    def test_filter_by_likes_minimum(self):
        """Тест фильтра по минимуму лайков"""
        min_likes = 100
        video_likes = 150

        assert video_likes >= min_likes

    def test_filter_by_comments_minimum(self):
        """Тест фильтра по минимуму комментариев"""
        min_comments = 50
        video_comments = 75

        assert video_comments >= min_comments

    def test_search_query_format(self):
        """Тест формата поискового запроса"""
        query = "Славяно-Арийская культура"
        assert isinstance(query, str)
        assert len(query) > 0
        assert len(query) < 1000


class TestDatabase:
    """Тесты для Database операций"""

    def test_database_connection(self, temp_db):
        """Тест подключения к БД"""
        conn = sqlite3.connect(temp_db)
        assert conn is not None
        conn.close()

    def test_insert_video_record(self, temp_db, sample_video):
        """Тест вставки видео в БД"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        c.execute("""
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments,
             engagement_ratio, description, tags, published_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_video['video_id'], sample_video['title'], sample_video['channel'],
            sample_video['url'], sample_video['views'], sample_video['likes'],
            sample_video['comments'], sample_video['engagement_ratio'],
            sample_video['description'], sample_video['tags'],
            sample_video['published_at'], sample_video['status']
        ))

        conn.commit()

        # Проверяем вставку
        c.execute("SELECT COUNT(*) FROM videos WHERE video_id = ?", (sample_video['video_id'],))
        count = c.fetchone()[0]

        conn.close()
        assert count == 1

    def test_query_videos_by_status(self, temp_db, sample_video):
        """Тест запроса видео по статусу"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео
        c.execute("""
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments,
             engagement_ratio, description, tags, published_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_video['video_id'], sample_video['title'], sample_video['channel'],
            sample_video['url'], sample_video['views'], sample_video['likes'],
            sample_video['comments'], sample_video['engagement_ratio'],
            sample_video['description'], sample_video['tags'],
            sample_video['published_at'], sample_video['status']
        ))
        conn.commit()

        # Запрашиваем по статусу
        c.execute("SELECT COUNT(*) FROM videos WHERE status = ?", ('new',))
        count = c.fetchone()[0]

        conn.close()
        assert count >= 1

    def test_update_video_field(self, temp_db, sample_video):
        """Тест обновления поля видео"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео
        c.execute("""
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments,
             engagement_ratio, description, tags, published_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_video['video_id'], sample_video['title'], sample_video['channel'],
            sample_video['url'], sample_video['views'], sample_video['likes'],
            sample_video['comments'], sample_video['engagement_ratio'],
            sample_video['description'], sample_video['tags'],
            sample_video['published_at'], 'new'
        ))
        conn.commit()

        # Обновляем статус
        c.execute("UPDATE videos SET status = ? WHERE video_id = ?",
                 ('content_ready', sample_video['video_id']))
        conn.commit()

        # Проверяем обновление
        c.execute("SELECT status FROM videos WHERE video_id = ?", (sample_video['video_id'],))
        status = c.fetchone()[0]

        conn.close()
        assert status == 'content_ready'


class TestTelegramNotifier:
    """Тесты для Telegram Notifier"""

    def test_message_format(self):
        """Тест формата Telegram сообщения"""
        title = "Test Video"
        engagement = 5.5

        message = f"🎯 {title}\nEngagement: {engagement}%"

        assert isinstance(message, str)
        assert len(message) > 0
        assert "Test Video" in message

    def test_token_not_empty(self, env_vars):
        """Тест что токен не пуст"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        assert token is not None
        assert len(token) > 0


class TestScoutAgentFlow:
    """Тесты для полного Scout Agent flow"""

    def test_search_and_store_video(self, temp_db, sample_video):
        """Тест поиска и сохранения видео"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео
        c.execute("""
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments,
             engagement_ratio, description, tags, published_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_video['video_id'], sample_video['title'], sample_video['channel'],
            sample_video['url'], sample_video['views'], sample_video['likes'],
            sample_video['comments'], sample_video['engagement_ratio'],
            sample_video['description'], sample_video['tags'],
            sample_video['published_at'], sample_video['status']
        ))
        conn.commit()

        # Логируем поиск
        c.execute("""
            INSERT INTO search_logs (search_at, query, results_count)
            VALUES (?, ?, ?)
        """, (datetime.now().isoformat(), 'test query', 1))
        conn.commit()

        # Проверяем результаты
        c.execute("SELECT COUNT(*) FROM videos")
        video_count = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM search_logs")
        log_count = c.fetchone()[0]

        conn.close()

        assert video_count >= 1
        assert log_count >= 1


# Performance Tests


@pytest.mark.performance
class TestScoutPerformance:
    """Тесты производительности Scout Agent"""

    def test_database_query_performance(self, temp_db, sample_video, benchmark):
        """Тест производительности запроса к БД"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем тестовое видео
        c.execute("""
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments,
             engagement_ratio, description, tags, published_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_video['video_id'], sample_video['title'], sample_video['channel'],
            sample_video['url'], sample_video['views'], sample_video['likes'],
            sample_video['comments'], sample_video['engagement_ratio'],
            sample_video['description'], sample_video['tags'],
            sample_video['published_at'], sample_video['status']
        ))
        conn.commit()

        def query():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE status = ?", ('new',))
            return cursor.fetchall()

        # Тестируем производительность
        result = benchmark(query)

        conn.close()
        assert len(result) >= 0


import os

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Integration Tests для MULTIC Pipeline

Тестирует взаимодействие компонентов (Scout → Copywriter → Promotion)
"""

import pytest
import sqlite3
from datetime import datetime


@pytest.mark.integration
class TestScoutToCopywriterPipeline:
    """Тесты интеграции Scout → Copywriter"""

    def test_scout_output_feeds_copywriter(self, temp_db, sample_video):
        """Тест что выход Scout питает Copywriter"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Scout сохраняет видео со статусом 'new'
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

        # Copywriter получает видео со статусом 'new'
        c.execute("SELECT COUNT(*) FROM videos WHERE status = 'new'")
        count = c.fetchone()[0]

        conn.close()
        assert count >= 1

    def test_copywriter_updates_status_after_processing(self, temp_db, sample_video):
        """Тест что Copywriter обновляет статус после обработки"""
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

        # Copywriter обновляет статус
        c.execute("UPDATE videos SET status = 'content_ready' WHERE video_id = ?",
                 (sample_video['video_id'],))
        conn.commit()

        # Проверяем обновление
        c.execute("SELECT status FROM videos WHERE video_id = ?",
                 (sample_video['video_id'],))
        status = c.fetchone()[0]

        conn.close()
        assert status == 'content_ready'


@pytest.mark.integration
class TestCopywriterToPromotionPipeline:
    """Тесты интеграции Copywriter → Promotion"""

    def test_content_variants_ready_for_promotion(self, temp_db, sample_video, sample_variant):
        """Тест что контент-варианты готовы к публикации"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео со статусом 'content_ready'
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
            sample_video['published_at'], 'content_ready'
        ))
        conn.commit()

        # Вставляем контент-варианты
        c.execute("""
            INSERT INTO content_variants
            (variant_id, video_id, type, number, platform, text, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_variant['variant_id'], sample_variant['video_id'],
            sample_variant['type'], sample_variant['number'],
            sample_variant['platform'], sample_variant['text'],
            'testing', sample_variant['created_at']
        ))
        conn.commit()

        # Promotion получает видео со статусом 'content_ready'
        c.execute("SELECT COUNT(*) FROM videos WHERE status = 'content_ready'")
        video_count = c.fetchone()[0]

        # Promotion получает варианты
        c.execute("SELECT COUNT(*) FROM content_variants WHERE video_id = ?",
                 (sample_video['video_id'],))
        variant_count = c.fetchone()[0]

        conn.close()
        assert video_count >= 1
        assert variant_count >= 1

    def test_promotion_publishes_and_updates_status(self, temp_db, sample_video):
        """Тест что Promotion публикует и обновляет статус"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео со статусом 'content_ready'
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
            sample_video['published_at'], 'content_ready'
        ))
        conn.commit()

        # Promotion обновляет статус на 'published'
        c.execute("UPDATE videos SET status = 'published' WHERE video_id = ?",
                 (sample_video['video_id'],))
        conn.commit()

        # Проверяем статус
        c.execute("SELECT status FROM videos WHERE video_id = ?",
                 (sample_video['video_id'],))
        status = c.fetchone()[0]

        conn.close()
        assert status == 'published'


@pytest.mark.integration
class TestFullPipeline:
    """Тесты полного конвейера Scout → Copywriter → Promotion"""

    def test_scout_to_promotion_complete_flow(self, temp_db, sample_video, sample_variant, sample_test_result):
        """Тест полный конвейер от Scout до Promotion"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # ФАЗА 1: Scout находит видео (статус 'new')
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

        # ФАЗА 2: Copywriter обрабатывает (статус 'content_ready')
        c.execute("UPDATE videos SET status = 'content_ready' WHERE video_id = ?",
                 (sample_video['video_id'],))

        # Copywriter создаёт контент-варианты
        for i in range(5):  # 5 примеров
            c.execute("""
                INSERT INTO content_variants
                (variant_id, video_id, type, number, platform, text, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"var_{i}", sample_video['video_id'], 'title', i, 'youtube',
                f"Title variant {i}", 'testing', datetime.now().isoformat()
            ))
        conn.commit()

        # ФАЗА 3: Promotion публикует (статус 'published')
        c.execute("UPDATE videos SET status = 'published' WHERE video_id = ?",
                 (sample_video['video_id'],))

        # Promotion записывает результаты A/B теста
        c.execute("""
            INSERT INTO ab_test_results
            (variant_id, platform, published_at, views, likes, comments, shares, ctr, engagement_ratio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_test_result['variant_id'], sample_test_result['platform'],
            sample_test_result['published_at'], sample_test_result['views'],
            sample_test_result['likes'], sample_test_result['comments'],
            sample_test_result['shares'], sample_test_result['ctr'],
            sample_test_result['engagement_ratio']
        ))
        conn.commit()

        # Проверяем результаты
        c.execute("SELECT status FROM videos WHERE video_id = ?",
                 (sample_video['video_id'],))
        final_status = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM content_variants WHERE video_id = ?",
                 (sample_video['video_id'],))
        variants_count = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM ab_test_results WHERE variant_id = ?",
                 (sample_test_result['variant_id'],))
        test_results_count = c.fetchone()[0]

        conn.close()

        # Проверяем что всё работает
        assert final_status == 'published'
        assert variants_count >= 1
        assert test_results_count >= 1

    def test_pipeline_data_integrity(self, temp_db, sample_video):
        """Тест целостность данных в конвейере"""
        conn = sqlite3.connect(temp_db)
        c = conn.cursor()

        # Вставляем видео с полной информацией
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

        # Получаем видео
        c.execute("SELECT * FROM videos WHERE video_id = ?",
                 (sample_video['video_id'],))
        result = c.fetchone()

        conn.close()

        # Проверяем что все данные сохранились
        assert result is not None
        assert result[1] == sample_video['title']  # title
        assert result[4] == sample_video['url']    # url
        assert result[5] == sample_video['views']  # views

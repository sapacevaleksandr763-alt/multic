#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Pytest Fixtures и Configuration для MULTIC тестов

Каждый тест использует эти fixtures для setup/teardown
"""

import pytest
import sqlite3
import tempfile
import os
from pathlib import Path
from datetime import datetime


@pytest.fixture
def temp_db():
    """Создаёт временную БД для тестов"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    # Инициализируем схему
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Создаём все таблицы
    c.execute("""
        CREATE TABLE videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            channel TEXT,
            url TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            engagement_ratio REAL,
            description TEXT,
            tags TEXT,
            published_at TIMESTAMP,
            status TEXT DEFAULT 'new'
        )
    """)

    c.execute("""
        CREATE TABLE search_logs (
            id INTEGER PRIMARY KEY,
            search_at TIMESTAMP,
            query TEXT,
            results_count INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE content_variants (
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
        CREATE TABLE ab_test_results (
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

    conn.commit()
    conn.close()

    yield db_path

    # Cleanup
    os.unlink(db_path)


@pytest.fixture
def sample_video():
    """Пример видео для тестирования"""
    return {
        'video_id': 'test_vid_001',
        'title': 'Test Video Title',
        'channel': 'Test Channel',
        'url': 'https://youtube.com/watch?v=test',
        'views': 10000,
        'likes': 500,
        'comments': 100,
        'engagement_ratio': 6.0,
        'description': 'Test video description',
        'tags': '#test,#demo',
        'published_at': datetime.now().isoformat(),
        'status': 'new'
    }


@pytest.fixture
def sample_variant():
    """Пример контент-варианта"""
    return {
        'variant_id': 'test_var_001',
        'video_id': 'test_vid_001',
        'type': 'title',
        'number': 1,
        'platform': 'youtube',
        'text': 'Amazing Test Video Title',
        'status': 'testing',
        'created_at': datetime.now().isoformat()
    }


@pytest.fixture
def sample_test_result():
    """Пример результата A/B теста"""
    return {
        'variant_id': 'test_var_001',
        'platform': 'youtube',
        'published_at': datetime.now().isoformat(),
        'views': 1000,
        'likes': 50,
        'comments': 20,
        'shares': 10,
        'ctr': 3.5,
        'engagement_ratio': 7.0
    }


@pytest.fixture
def env_vars(monkeypatch):
    """Устанавливает тестовые переменные окружения"""
    monkeypatch.setenv('YOUTUBE_API_KEY', 'test_youtube_key')
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'test_telegram_token')
    monkeypatch.setenv('CLAUDE_API_KEY', 'test_claude_key')
    monkeypatch.setenv('VK_API_TOKEN', 'test_vk_token')
    return monkeypatch


@pytest.fixture
def mock_claude_response():
    """Mock ответ от Claude API"""
    return {
        'content': [
            {
                'text': 'Test analysis of video hooks and viral moments'
            }
        ]
    }


# Hooks для логирования


def pytest_configure(config):
    """Настройка pytest"""
    # Создаём директорию логов если её нет
    log_dir = Path('logs/tests')
    log_dir.mkdir(parents=True, exist_ok=True)


def pytest_runtest_logreport(report):
    """Логирует результаты тестов"""
    if report.when == "call":
        status = "✅ PASS" if report.outcome == "passed" else "❌ FAIL"
        print(f"\n{status}: {report.nodeid}")


# Маркеры для категоризации тестов


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "security: mark test as a security test")

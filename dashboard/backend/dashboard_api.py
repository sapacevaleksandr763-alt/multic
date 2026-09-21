#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Master Dashboard Backend API

FastAPI сервер для MULTIC Master Dashboard

Endpoints:
- GET /api/dashboard - получить все данные
- GET /api/scout - данные Scout Agent
- GET /api/copywriter - данные Copywriter Agent
- GET /api/promotion - данные Promotion Agent
- GET /api/analytics - данные Analytics
- POST /api/scout/run - запустить Scout Agent
- POST /api/copywriter/run - запустить Copywriter Agent
- POST /api/promotion/run - запустить Promotion Agent
- WS /ws/dashboard - WebSocket real-time updates
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import json

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="MULTIC Dashboard API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = '../../../scout_agent.db'


class DashboardDataCollector:
    """Собирает данные из всех компонентов системы"""

    @staticmethod
    def get_scout_data() -> Dict[str, Any]:
        """Получает данные Scout Agent"""
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            # Получаем статистику за день
            today = datetime.now().date()
            c.execute("""
                SELECT COUNT(*) FROM videos WHERE DATE(published_at) = ?
            """, (today,))
            videos_today = c.fetchone()[0]

            # Всего видео
            c.execute("SELECT COUNT(*) FROM videos")
            total_videos = c.fetchone()[0]

            # Средний engagement
            c.execute("SELECT AVG(engagement_ratio) FROM videos")
            avg_engagement = c.fetchone()[0] or 0

            # Последний поиск
            c.execute("SELECT MAX(search_at) FROM search_logs")
            last_search = c.fetchone()[0] or datetime.now().isoformat()

            conn.close()

            return {
                "videos_found_today": videos_today,
                "total_videos": total_videos,
                "engagement_ratio_avg": avg_engagement,
                "last_search": last_search,
                "status": "running"
            }
        except Exception as e:
            logger.error(f"Error collecting Scout data: {e}")
            return {
                "videos_found_today": 0,
                "total_videos": 0,
                "engagement_ratio_avg": 0.0,
                "last_search": datetime.now().isoformat(),
                "status": "error"
            }

    @staticmethod
    def get_copywriter_data() -> Dict[str, Any]:
        """Получает данные Copywriter Agent"""
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            # Видео в обработке
            c.execute("SELECT COUNT(*) FROM videos WHERE status = 'content_ready'")
            videos_analyzing = c.fetchone()[0]

            # Варианты созданы
            c.execute("SELECT COUNT(*) FROM content_variants")
            variants_generated = c.fetchone()[0]

            conn.close()

            return {
                "videos_analyzing": videos_analyzing,
                "variants_generated": variants_generated,
                "status": "processing" if videos_analyzing > 0 else "idle"
            }
        except Exception as e:
            logger.error(f"Error collecting Copywriter data: {e}")
            return {
                "videos_analyzing": 0,
                "variants_generated": 0,
                "status": "error"
            }

    @staticmethod
    def get_promotion_data() -> Dict[str, Any]:
        """Получает данные Promotion Agent"""
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            # Видео опубликовано
            c.execute("SELECT COUNT(*) FROM videos WHERE status = 'published'")
            published = c.fetchone()[0]

            # Просмотры
            c.execute("SELECT SUM(views) FROM videos WHERE status = 'published'")
            total_views = c.fetchone()[0] or 0

            conn.close()

            return {
                "videos_published": published,
                "platforms_active": 6,  # 6 платформ поддерживаются
                "total_views": total_views,
                "status": "ready"
            }
        except Exception as e:
            logger.error(f"Error collecting Promotion data: {e}")
            return {
                "videos_published": 0,
                "platforms_active": 0,
                "total_views": 0,
                "status": "error"
            }

    @staticmethod
    def get_analytics_data() -> Dict[str, Any]:
        """Получает данные Analytics"""
        try:
            # Для демо используем симуляцию
            # В production это будет из реальных API платформ
            return {
                "youtube_views": 20000,
                "telegram_views": 8000,
                "vk_views": 12000,
                "instagram_views": 3000,
                "avg_engagement": 2.8
            }
        except Exception as e:
            logger.error(f"Error collecting Analytics data: {e}")
            return {
                "youtube_views": 0,
                "telegram_views": 0,
                "vk_views": 0,
                "instagram_views": 0,
                "avg_engagement": 0.0
            }


# API Endpoints


@app.get("/api/dashboard")
async def get_dashboard_data():
    """Получить все данные Dashboard"""
    collector = DashboardDataCollector()

    return {
        "scout": collector.get_scout_data(),
        "copywriter": collector.get_copywriter_data(),
        "promotion": collector.get_promotion_data(),
        "analytics": collector.get_analytics_data()
    }


@app.get("/api/scout")
async def get_scout():
    """Получить данные Scout Agent"""
    collector = DashboardDataCollector()
    return collector.get_scout_data()


@app.get("/api/copywriter")
async def get_copywriter():
    """Получить данные Copywriter Agent"""
    collector = DashboardDataCollector()
    return collector.get_copywriter_data()


@app.get("/api/promotion")
async def get_promotion():
    """Получить данные Promotion Agent"""
    collector = DashboardDataCollector()
    return collector.get_promotion_data()


@app.get("/api/analytics")
async def get_analytics():
    """Получить данные Analytics"""
    collector = DashboardDataCollector()
    return collector.get_analytics_data()


@app.post("/api/scout/run")
async def run_scout():
    """Запустить Scout Agent"""
    logger.info("Manual trigger: Running Scout Agent")
    # TODO: Интегрировать с фактическим Scout Agent
    return {"status": "started", "message": "Scout Agent запущен"}


@app.post("/api/copywriter/run")
async def run_copywriter():
    """Запустить Copywriter Agent"""
    logger.info("Manual trigger: Running Copywriter Agent")
    # TODO: Интегрировать с фактическим Copywriter Agent
    return {"status": "started", "message": "Copywriter Agent запущен"}


@app.post("/api/promotion/run")
async def run_promotion():
    """Запустить Promotion Agent"""
    logger.info("Manual trigger: Running Promotion Agent")
    # TODO: Интегрировать с фактическим Promotion Agent
    return {"status": "started", "message": "Promotion Agent запущен"}


# WebSocket для real-time обновлений
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")


manager = ConnectionManager()


@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    """WebSocket endpoint для real-time updates"""
    await manager.connect(websocket)
    collector = DashboardDataCollector()

    try:
        while True:
            # Отправляем обновления каждые 5 секунд
            await asyncio.sleep(5)

            data = {
                "scout": collector.get_scout_data(),
                "copywriter": collector.get_copywriter_data(),
                "promotion": collector.get_promotion_data(),
                "analytics": collector.get_analytics_data(),
                "timestamp": datetime.now().isoformat()
            }

            await websocket.send_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    print("🎬 MULTIC Dashboard API Starting...")
    print("📊 Dashboard available at http://localhost:8000")
    print("🔗 WebSocket at ws://localhost:8000/ws/dashboard")

    uvicorn.run(app, host="0.0.0.0", port=8000)

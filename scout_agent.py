#!/usr/bin/env python3
"""
🔍 Scout Agent - Поиск вирусных видео по тематике

Основная функция:
- Поиск видео на YouTube по запросу "Славяно-Арийская культура"
- Фильтрация по лайкам (>100) и комментариям (>50)
- Отправка ТОП-5 видео в Telegram
- Логирование всех результатов в SQLite БД
"""

import logging
import asyncio
import time
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from config import SEARCH_FREQUENCY, LOG_DIR
from youtube_searcher import YouTubeSearcher
from telegram_notifier import TelegramNotifier
from database import ScoutDatabase

# Настройка логирования
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{LOG_DIR}/scout_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ScoutAgent:
    def __init__(self):
        self.searcher = YouTubeSearcher()
        self.notifier = TelegramNotifier()
        self.database = ScoutDatabase()
        self.scheduler = BackgroundScheduler()

    async def run_search(self):
        """Выполнить поиск видео и отправить результаты"""
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("🔍 Scout Agent: Начало поиска видео")
        logger.info("=" * 60)

        try:
            # Поиск видео
            videos = self.searcher.find_top_videos()

            # Проверка новых видео
            new_videos = []
            for video in videos:
                if not self.database.video_exists(video['video_id']):
                    self.database.add_video(video)
                    new_videos.append(video)

            execution_time = time.time() - start_time

            logger.info(f"✅ Найдено видео: {len(videos)}")
            logger.info(f"📝 Новых видео в БД: {len(new_videos)}")
            logger.info(f"⏱️ Время выполнения: {execution_time:.2f} сек")

            # Отправить результаты в Telegram
            if new_videos:
                success = await self.notifier.send_video_messages(new_videos)
                telegram_status = 'success' if success else 'failed'
            else:
                logger.info("ℹ️ Новых видео не найдено (все видео уже в БД)")
                telegram_status = 'no_new_videos'

            # Логировать результаты в БД
            self.database.log_search(
                videos_found=len(videos),
                top_videos_sent=len(new_videos),
                status=telegram_status,
                execution_time=execution_time
            )

            logger.info("=" * 60)
            logger.info(f"✅ Поиск завершен успешно")
            logger.info("=" * 60)

            return True

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ Ошибка при поиске: {str(e)}", exc_info=True)

            # Логировать ошибку
            self.database.log_search(
                videos_found=0,
                top_videos_sent=0,
                status='error',
                error_message=str(e),
                execution_time=execution_time
            )

            # Отправить уведомление об ошибке в Telegram
            await self.notifier.send_error_notification(str(e))

            logger.info("=" * 60)
            return False

    def start_scheduler(self):
        """Запустить планировщик для автоматического поиска"""
        logger.info("🕐 Инициализация планировщика")

        # Установить временную зону (МСК)
        msk = timezone('Europe/Moscow')

        # Добавить задачу для ежедневного поиска в 09:00 МСК
        self.scheduler.add_job(
            func=self._async_job_wrapper,
            trigger="cron",
            hour=9,
            minute=0,
            timezone=msk,
            id='daily_search',
            name='Daily Video Search',
            replace_existing=True
        )

        logger.info("📅 Расписание добавлено: каждый день в 09:00 МСК")

        self.scheduler.start()
        logger.info("✅ Планировщик запущен")

    def _async_job_wrapper(self):
        """Обертка для запуска async функции в планировщике"""
        asyncio.run(self.run_search())

    async def run_once(self):
        """Запустить поиск один раз (для тестирования)"""
        logger.info("🚀 Запуск Scout Agent (один раз)")
        return await self.run_search()

    def stop_scheduler(self):
        """Остановить планировщик"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("✅ Планировщик остановлен")

async def main():
    """Главная функция"""
    agent = ScoutAgent()

    # Запустить поиск один раз для тестирования
    logger.info("\n" + "="*60)
    logger.info("🚀 SCOUT AGENT - FIRST RUN TEST")
    logger.info("="*60 + "\n")

    await agent.run_once()

    # Запустить планировщик для автоматического выполнения
    logger.info("\n" + "="*60)
    logger.info("🕐 STARTING SCHEDULER FOR DAILY RUNS")
    logger.info("="*60 + "\n")

    agent.start_scheduler()

    try:
        # Держать программу в работе
        logger.info("⏳ Scout Agent активен и готов к работе...")
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Остановка Scout Agent...")
        agent.stop_scheduler()

if __name__ == "__main__":
    asyncio.run(main())

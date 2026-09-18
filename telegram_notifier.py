import logging
import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self, bot_token=TELEGRAM_BOT_TOKEN):
        self.bot_token = bot_token
        self.channel_id = TELEGRAM_CHANNEL_ID
        self.bot = None

        if bot_token:
            self.bot = Bot(token=bot_token)

    def format_video_message(self, video_data, rank):
        """Форматировать сообщение о видео для Telegram"""
        title = video_data['title'][:100]
        channel = video_data['channel'][:50]
        views_str = self._format_number(video_data['views'])
        likes_str = self._format_number(video_data['likes'])
        comments_str = self._format_number(video_data['comments'])
        engagement = video_data['engagement_ratio']
        url = video_data['url']

        message = f"""📺 <b>[ТОП {rank}/5] {title}</b>

👤 <b>Канал:</b> {channel}
👁️ <b>Просмотры:</b> {views_str} | 👍 <b>Лайки:</b> {likes_str} | 💬 <b>Комментарии:</b> {comments_str}
⚡ <b>Engagement:</b> {engagement}%

🔗 <a href="{url}">Смотреть видео</a>
"""
        return message

    def format_summary_message(self, videos_data):
        """Форматировать сводку найденных видео"""
        message = "📊 <b>РЕЗУЛЬТАТЫ ПОИСКА ВИРУСНЫХ ВИДЕО</b> 📊\n\n"
        message += f"🔍 Найдено видео: {len(videos_data)}\n"
        message += f"⭐ Лучший engagement: {videos_data[0]['engagement_ratio']}%\n"
        message += f"📅 Дата поиска: {videos_data[0].get('published_at', 'N/A')[:10]}\n\n"

        message += "━━━━━━━━━━━━━━━━━\n\n"

        for idx, video in enumerate(videos_data, 1):
            message += f"{idx}. <b>{video['title'][:60]}...</b>\n"
            message += f"   👤 {video['channel'][:40]}\n"
            message += f"   ⚡ {video['engagement_ratio']}% engagement\n"
            message += f"   🔗 https://youtu.be/{video['video_id']}\n\n"

        return message

    @staticmethod
    def _format_number(num):
        """Форматировать число для удобочитаемости (1500 -> 1.5K, 1500000 -> 1.5M)"""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)

    async def send_video_messages(self, videos_data):
        """Отправить сообщения о каждом видео в Telegram"""
        if not self.bot:
            logger.warning("Telegram Bot Token не установлен. Сообщения не отправлены.")
            return False

        if not videos_data:
            logger.info("Нет видео для отправки")
            return True

        try:
            # Отправить сводку
            summary_msg = self.format_summary_message(videos_data)
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=summary_msg,
                parse_mode='HTML'
            )
            logger.info("Сводка отправлена в Telegram")

            # Отправить детальное сообщение для каждого видео
            for idx, video in enumerate(videos_data, 1):
                message = self.format_video_message(video, idx)
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message,
                    parse_mode='HTML'
                )

                # Небольшая задержка между сообщениями
                await asyncio.sleep(0.5)

            logger.info(f"Отправлено {len(videos_data)} сообщений в Telegram")
            return True

        except Exception as e:
            logger.error(f"Ошибка при отправке в Telegram: {str(e)}")
            return False

    async def send_error_notification(self, error_message):
        """Отправить уведомление об ошибке в Telegram"""
        if not self.bot:
            return False

        try:
            message = f"⚠️ <b>ОШИБКА Scout Agent:</b>\n\n{error_message}"
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='HTML'
            )
            logger.info("Уведомление об ошибке отправлено в Telegram")
            return True
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления об ошибке: {str(e)}")
            return False

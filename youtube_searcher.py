import logging
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from config import (
    YOUTUBE_API_KEY, SEARCH_TOPIC, SEARCH_MIN_LIKES,
    SEARCH_MIN_COMMENTS, SEARCH_TOP_VIDEOS
)

logger = logging.getLogger(__name__)

class YouTubeSearcher:
    def __init__(self, api_key=YOUTUBE_API_KEY):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def search_videos(self, query, max_results=50):
        """Поиск видео по запросу на YouTube"""
        try:
            # Поиск видео за последние 30 дней
            published_after = (datetime.now() - timedelta(days=30)).isoformat() + 'Z'

            request = self.youtube.search().list(
                q=query,
                type='video',
                part='snippet',
                maxResults=min(max_results, 50),
                order='relevance',
                publishedAfter=published_after,
                regionCode='RU',
                relevanceLanguage='ru'
            )

            response = request.execute()
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]

            logger.info(f"Найдено {len(video_ids)} видео по запросу: {query}")
            return video_ids

        except Exception as e:
            logger.error(f"Ошибка при поиске видео: {str(e)}")
            return []

    def get_video_stats(self, video_ids):
        """Получить статистику для видео (просмотры, лайки, комментарии)"""
        if not video_ids:
            return []

        try:
            videos_data = []

            for video_id in video_ids:
                try:
                    # Получить статистику видео
                    request = self.youtube.videos().list(
                        part='statistics,snippet,contentDetails',
                        id=video_id
                    )
                    response = request.execute()

                    if response['items']:
                        item = response['items'][0]
                        snippet = item['snippet']
                        stats = item['statistics']

                        views = int(stats.get('viewCount', 0))
                        likes = int(stats.get('likeCount', 0)) if 'likeCount' in stats else 0
                        comments = int(stats.get('commentCount', 0)) if 'commentCount' in stats else 0

                        # Фильтр по минимальному кол-ву лайков и комментариев
                        if likes >= SEARCH_MIN_LIKES and comments >= SEARCH_MIN_COMMENTS:
                            engagement_ratio = ((likes + comments) / views * 100) if views > 0 else 0

                            video_data = {
                                'video_id': video_id,
                                'title': snippet['title'],
                                'channel': snippet['channelTitle'],
                                'url': f"https://www.youtube.com/watch?v={video_id}",
                                'views': views,
                                'likes': likes,
                                'comments': comments,
                                'engagement_ratio': round(engagement_ratio, 2),
                                'description': snippet.get('description', '')[:500],
                                'tags': snippet.get('tags', []),
                                'published_at': snippet['publishedAt'],
                                'thumbnail': snippet['thumbnails']['medium']['url']
                            }
                            videos_data.append(video_data)

                except Exception as e:
                    logger.warning(f"Ошибка при получении статистики для видео {video_id}: {str(e)}")
                    continue

            # Сортировать по engagement ratio (по убыванию)
            videos_data.sort(key=lambda x: x['engagement_ratio'], reverse=True)

            logger.info(f"Отфильтровано {len(videos_data)} видео с нужной статистикой")
            return videos_data[:SEARCH_TOP_VIDEOS]  # Вернуть топ N видео

        except Exception as e:
            logger.error(f"Ошибка при получении статистики видео: {str(e)}")
            return []

    def find_top_videos(self, query=SEARCH_TOPIC):
        """Найти топ видео по тематике"""
        logger.info(f"Начинаем поиск видео: {query}")

        # Поиск видео
        video_ids = self.search_videos(query, max_results=50)

        if not video_ids:
            logger.warning("Видео не найдены")
            return []

        # Получить статистику
        top_videos = self.get_video_stats(video_ids)

        logger.info(f"Найдено {len(top_videos)} топ-видео")
        return top_videos

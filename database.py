import sqlite3
import json
from datetime import datetime
from config import DATABASE_FILE

class ScoutDatabase:
    def __init__(self, db_file=DATABASE_FILE):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                channel TEXT NOT NULL,
                url TEXT NOT NULL,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                engagement_ratio REAL,
                description TEXT,
                tags TEXT,
                published_at TEXT,
                date_found TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_date TEXT NOT NULL,
                videos_found INTEGER,
                top_videos_sent INTEGER,
                status TEXT DEFAULT 'success',
                error_message TEXT,
                execution_time_sec REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def video_exists(self, video_id):
        """Проверить, существует ли видео в БД"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('SELECT id FROM videos WHERE video_id = ?', (video_id,))
        result = c.fetchone()
        conn.close()
        return result is not None

    def add_video(self, video_data):
        """Добавить видео в БД"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''
            INSERT INTO videos
            (video_id, title, channel, url, views, likes, comments, engagement_ratio,
             description, tags, published_at, date_found, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_data['video_id'],
            video_data['title'],
            video_data['channel'],
            video_data['url'],
            video_data.get('views', 0),
            video_data.get('likes', 0),
            video_data.get('comments', 0),
            video_data.get('engagement_ratio', 0),
            video_data.get('description', ''),
            json.dumps(video_data.get('tags', [])),
            video_data.get('published_at', ''),
            datetime.now().strftime('%Y-%m-%d'),
            'new'
        ))

        conn.commit()
        conn.close()

    def log_search(self, videos_found, top_videos_sent, status='success',
                   error_message=None, execution_time=0):
        """Логировать результаты поиска"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('''
            INSERT INTO search_logs
            (search_date, videos_found, top_videos_sent, status, error_message, execution_time_sec)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            videos_found,
            top_videos_sent,
            status,
            error_message,
            execution_time
        ))

        conn.commit()
        conn.close()

    def get_videos_by_date(self, date_str):
        """Получить все видео, найденные в конкретную дату"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM videos WHERE date_found = ? ORDER BY engagement_ratio DESC', (date_str,))
        result = c.fetchall()
        conn.close()
        return result

    def update_video_status(self, video_id, status):
        """Обновить статус видео (new/analyzing/analyzed)"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('UPDATE videos SET status = ? WHERE video_id = ?', (status, video_id))
        conn.commit()
        conn.close()

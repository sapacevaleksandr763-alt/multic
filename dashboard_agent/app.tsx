"""React App for Master Dashboard - generated as TypeScript"""

import React, { useState, useEffect } from 'react';
import './Dashboard.css';

interface PlatformMetrics {
  platform: string;
  total_videos: number;
  total_views: number;
  total_likes: number;
  total_comments: number;
  total_shares: number;
  average_engagement_rate: number;
  total_reach: number;
  last_updated: string;
}

interface VideoAnalytics {
  video_id: string;
  title: string;
  original_platform: string;
  total_views: number;
  total_engagement: number;
  top_platform: string;
  published_at: string;
}

interface DashboardStats {
  total_videos_found: number;
  total_videos_published: number;
  total_videos_pending: number;
  total_views_all_platforms: number;
  total_engagement_all_platforms: number;
  average_engagement_rate: number;
  platforms: Record<string, PlatformMetrics>;
  videos: Record<string, VideoAnalytics>;
  total_posts_created: number;
  total_posts_published: number;
  republish_count: number;
  last_updated: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'platforms' | 'videos' | 'events'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    // Refresh every 5 minutes
    const interval = setInterval(fetchDashboardData, 300000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/dashboard/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return <div className="dashboard-loading">📊 Loading Dashboard...</div>;
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🎬 MULTIC Master Dashboard</h1>
          <p>Real-time Publishing & Analytics</p>
        </div>
        <div className="header-actions">
          <button onClick={fetchDashboardData} className="btn-refresh">
            🔄 Refresh
          </button>
          <span className="last-updated">
            Last updated: {new Date(stats.last_updated).toLocaleTimeString()}
          </span>
        </div>
      </header>

      {/* Navigation */}
      <nav className="dashboard-nav">
        <button
          className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`nav-item ${activeTab === 'platforms' ? 'active' : ''}`}
          onClick={() => setActiveTab('platforms')}
        >
          📱 Platforms
        </button>
        <button
          className={`nav-item ${activeTab === 'videos' ? 'active' : ''}`}
          onClick={() => setActiveTab('videos')}
        >
          🎥 Videos
        </button>
        <button
          className={`nav-item ${activeTab === 'events' ? 'active' : ''}`}
          onClick={() => setActiveTab('events')}
        >
          📝 Events
        </button>
      </nav>

      {/* Content */}
      <main className="dashboard-content">
        {activeTab === 'overview' && (
          <OverviewTab stats={stats} />
        )}
        {activeTab === 'platforms' && (
          <PlatformsTab stats={stats} />
        )}
        {activeTab === 'videos' && (
          <VideosTab stats={stats} />
        )}
        {activeTab === 'events' && (
          <EventsTab stats={stats} />
        )}
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>Phase 2C: Promotion Agent | Phase 2D: Master Dashboard</p>
      </footer>
    </div>
  );
};

// Overview Tab Component
const OverviewTab: React.FC<{ stats: DashboardStats }> = ({ stats }) => {
  return (
    <div className="tab-content">
      <section className="stats-grid">
        {/* KPI Cards */}
        <div className="stat-card primary">
          <h3>📊 Total Videos</h3>
          <p className="stat-value">{stats.total_videos_found}</p>
          <p className="stat-detail">
            ✅ {stats.total_videos_published} published | ⏳ {stats.total_videos_pending} pending
          </p>
        </div>

        <div className="stat-card primary">
          <h3>👁️ Total Views</h3>
          <p className="stat-value">{stats.total_views_all_platforms.toLocaleString()}</p>
          <p className="stat-detail">Across all platforms</p>
        </div>

        <div className="stat-card primary">
          <h3>❤️ Total Engagement</h3>
          <p className="stat-value">{stats.total_engagement_all_platforms.toLocaleString()}</p>
          <p className="stat-detail">{stats.average_engagement_rate.toFixed(2)}% rate</p>
        </div>

        <div className="stat-card secondary">
          <h3>📱 Posts Created</h3>
          <p className="stat-value">{stats.total_posts_created}</p>
          <p className="stat-detail">✅ {stats.total_posts_published} published</p>
        </div>

        <div className="stat-card secondary">
          <h3>🔄 Republishes</h3>
          <p className="stat-value">{stats.republish_count}</p>
          <p className="stat-detail">Evergreen content</p>
        </div>

        <div className="stat-card secondary">
          <h3>📈 Platforms Active</h3>
          <p className="stat-value">{Object.keys(stats.platforms).length}</p>
          <p className="stat-detail">YouTube, Telegram, TikTok, Instagram, RuTube, VK, OK.ru</p>
        </div>
      </section>

      {/* Platform Performance */}
      <section className="performance-section">
        <h2>Platform Performance</h2>
        <div className="platform-grid">
          {Object.entries(stats.platforms).map(([platform, metrics]) => (
            <div key={platform} className="platform-card">
              <h3>{platform.toUpperCase()}</h3>
              <div className="metrics">
                <div className="metric">
                  <span className="label">Videos</span>
                  <span className="value">{metrics.total_videos}</span>
                </div>
                <div className="metric">
                  <span className="label">Views</span>
                  <span className="value">{metrics.total_views.toLocaleString()}</span>
                </div>
                <div className="metric">
                  <span className="label">Engagement</span>
                  <span className="value">
                    {(metrics.total_likes + metrics.total_comments + metrics.total_shares).toLocaleString()}
                  </span>
                </div>
                <div className="metric">
                  <span className="label">Rate</span>
                  <span className="value">{metrics.average_engagement_rate.toFixed(2)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

// Platforms Tab Component
const PlatformsTab: React.FC<{ stats: DashboardStats }> = ({ stats }) => {
  return (
    <div className="tab-content">
      <h2>📱 Platform Analytics</h2>
      <table className="analytics-table">
        <thead>
          <tr>
            <th>Platform</th>
            <th>Videos</th>
            <th>Total Views</th>
            <th>Likes</th>
            <th>Comments</th>
            <th>Shares</th>
            <th>Engagement Rate</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(stats.platforms).map(([_, metrics]) => (
            <tr key={metrics.platform}>
              <td className="platform-name">{metrics.platform.toUpperCase()}</td>
              <td>{metrics.total_videos}</td>
              <td>{metrics.total_views.toLocaleString()}</td>
              <td>{metrics.total_likes.toLocaleString()}</td>
              <td>{metrics.total_comments.toLocaleString()}</td>
              <td>{metrics.total_shares.toLocaleString()}</td>
              <td className="engagement">
                <span className={metrics.average_engagement_rate > 0.05 ? 'high' : 'low'}>
                  {metrics.average_engagement_rate.toFixed(2)}%
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Videos Tab Component
const VideosTab: React.FC<{ stats: DashboardStats }> = ({ stats }) => {
  const sortedVideos = Object.entries(stats.videos)
    .sort(([, a], [, b]) => b.total_views - a.total_views)
    .slice(0, 10);

  return (
    <div className="tab-content">
      <h2>🎥 Top Videos</h2>
      <div className="videos-list">
        {sortedVideos.map(([videoId, video]) => (
          <div key={videoId} className="video-card">
            <div className="video-header">
              <h3>{video.title}</h3>
              <span className="badge">{video.original_platform}</span>
            </div>
            <div className="video-metrics">
              <div className="metric">
                <span>👁️ Views:</span>
                <strong>{video.total_views.toLocaleString()}</strong>
              </div>
              <div className="metric">
                <span>❤️ Engagement:</span>
                <strong>{video.total_engagement.toLocaleString()}</strong>
              </div>
              <div className="metric">
                <span>📊 Top Platform:</span>
                <strong>{video.top_platform || 'N/A'}</strong>
              </div>
              <div className="metric">
                <span>📅 Published:</span>
                <strong>{new Date(video.published_at).toLocaleDateString()}</strong>
              </div>
            </div>
            <div className="video-actions">
              <button className="btn-small" data-video-id={videoId}>
                📊 Details
              </button>
              <button className="btn-small" data-video-id={videoId}>
                🔄 Republish
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Events Tab Component
const EventsTab: React.FC<{ stats: DashboardStats }> = ({ stats }) => {
  return (
    <div className="tab-content">
      <h2>📝 Recent Events</h2>
      <div className="events-timeline">
        <div className="event">
          <span className="event-time">Just now</span>
          <span className="event-type">📊 Dashboard Updated</span>
          <span className="event-detail">Analytics refreshed</span>
        </div>
        <div className="event">
          <span className="event-time">2 hours ago</span>
          <span className="event-type">✅ Video Published</span>
          <span className="event-detail">Published to 7 platforms</span>
        </div>
        <div className="event">
          <span className="event-time">1 day ago</span>
          <span className="event-type">📱 Posts Generated</span>
          <span className="event-detail">7 platform-specific posts created</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

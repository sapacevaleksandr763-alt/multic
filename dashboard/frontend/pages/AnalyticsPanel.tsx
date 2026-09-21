import React from 'react'

interface AnalyticsData {
  youtube_views: number
  telegram_views: number
  vk_views: number
  instagram_views: number
  avg_engagement: number
}

interface Props {
  data: AnalyticsData
}

const AnalyticsPanel: React.FC<Props> = ({ data }) => {
  const totalViews = data.youtube_views + data.telegram_views + data.vk_views + data.instagram_views

  const getPlatformPercentage = (views: number) => {
    return totalViews > 0 ? ((views / totalViews) * 100).toFixed(1) : '0.0'
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">📊 ANALYTICS</h2>
        <span className="panel-status status-running">Live</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Всего просмотров</span>
        <span className="metric-value">{(totalViews / 1000).toFixed(1)}K</span>
      </div>

      <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #374151' }}>
        <div className="metric-row">
          <span className="metric-label">YouTube</span>
          <span className="metric-value" style={{ fontSize: '1.125rem' }}>
            {data.youtube_views.toLocaleString()} ({getPlatformPercentage(data.youtube_views)}%)
          </span>
        </div>

        <div className="metric-row">
          <span className="metric-label">Telegram</span>
          <span className="metric-value" style={{ fontSize: '1.125rem' }}>
            {data.telegram_views.toLocaleString()} ({getPlatformPercentage(data.telegram_views)}%)
          </span>
        </div>

        <div className="metric-row">
          <span className="metric-label">VK</span>
          <span className="metric-value" style={{ fontSize: '1.125rem' }}>
            {data.vk_views.toLocaleString()} ({getPlatformPercentage(data.vk_views)}%)
          </span>
        </div>

        <div className="metric-row">
          <span className="metric-label">Instagram</span>
          <span className="metric-value" style={{ fontSize: '1.125rem' }}>
            {data.instagram_views.toLocaleString()} ({getPlatformPercentage(data.instagram_views)}%)
          </span>
        </div>
      </div>

      <div className="metric-row" style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #374151' }}>
        <span className="metric-label">Средний engagement</span>
        <span className="metric-value">{data.avg_engagement.toFixed(2)}%</span>
      </div>
    </div>
  )
}

export default AnalyticsPanel

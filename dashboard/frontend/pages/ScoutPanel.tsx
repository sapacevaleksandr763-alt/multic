import React from 'react'

interface ScoutData {
  videos_found_today: number
  total_videos: number
  engagement_ratio_avg: number
  last_search: string
  status: string
}

interface Props {
  data: ScoutData
}

const ScoutPanel: React.FC<Props> = ({ data }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'status-running'
      case 'error':
        return 'status-error'
      default:
        return 'status-idle'
    }
  }

  const runScoutNow = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/scout/run', { method: 'POST' })
      if (response.ok) {
        alert('Scout Agent запущен')
      }
    } catch (error) {
      console.error('Failed to run Scout Agent:', error)
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">🔍 SCOUT AGENT</h2>
        <span className={`panel-status ${getStatusColor(data.status)}`}>{data.status}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Видео найдено сегодня</span>
        <span className="metric-value">{data.videos_found_today}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Всего видео</span>
        <span className="metric-value">{data.total_videos}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Средний engagement</span>
        <span className="metric-value">{data.engagement_ratio_avg.toFixed(1)}%</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Последний поиск</span>
        <span className="metric-value" style={{ fontSize: '0.875rem' }}>
          {new Date(data.last_search).toLocaleTimeString()}
        </span>
      </div>

      <button className="btn" onClick={runScoutNow}>
        Run Scout Agent
      </button>
    </div>
  )
}

export default ScoutPanel

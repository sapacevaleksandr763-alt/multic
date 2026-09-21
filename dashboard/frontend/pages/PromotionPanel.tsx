import React from 'react'

interface PromotionData {
  videos_published: number
  platforms_active: number
  total_views: number
  status: string
}

interface Props {
  data: PromotionData
}

const PromotionPanel: React.FC<Props> = ({ data }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready':
        return 'status-running'
      case 'publishing':
        return 'status-processing'
      default:
        return 'status-idle'
    }
  }

  const runPromotion = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/promotion/run', { method: 'POST' })
      if (response.ok) {
        alert('Promotion Agent запущен')
      }
    } catch (error) {
      console.error('Failed to run Promotion Agent:', error)
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">🎬 PROMOTION AGENT</h2>
        <span className={`panel-status ${getStatusColor(data.status)}`}>{data.status}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Видео опубликовано</span>
        <span className="metric-value">{data.videos_published}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Активные платформы</span>
        <span className="metric-value">{data.platforms_active}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Всего просмотров</span>
        <span className="metric-value">{(data.total_views / 1000).toFixed(1)}K</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Платформы</span>
        <span className="metric-value" style={{ fontSize: '0.75rem' }}>
          YT, TG, VK, RuTube, IG, OK.ru
        </span>
      </div>

      <button className="btn" onClick={runPromotion}>
        Run Promotion Agent
      </button>
    </div>
  )
}

export default PromotionPanel

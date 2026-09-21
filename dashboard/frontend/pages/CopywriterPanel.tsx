import React from 'react'

interface CopywriterData {
  videos_analyzing: number
  variants_generated: number
  status: string
}

interface Props {
  data: CopywriterData
}

const CopywriterPanel: React.FC<Props> = ({ data }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'processing':
        return 'status-processing'
      case 'idle':
        return 'status-idle'
      default:
        return 'status-idle'
    }
  }

  const runCopywriter = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/copywriter/run', { method: 'POST' })
      if (response.ok) {
        alert('Copywriter Agent запущен')
      }
    } catch (error) {
      console.error('Failed to run Copywriter Agent:', error)
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">✍️ COPYWRITER AGENT</h2>
        <span className={`panel-status ${getStatusColor(data.status)}`}>{data.status}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Видео в обработке</span>
        <span className="metric-value">{data.videos_analyzing}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Варианты созданы</span>
        <span className="metric-value">{data.variants_generated}</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Вариантов per видео</span>
        <span className="metric-value">55</span>
      </div>

      <div className="metric-row">
        <span className="metric-label">Статус</span>
        <span className="metric-value" style={{ fontSize: '0.875rem', color: '#10B981' }}>
          ✓ Ready
        </span>
      </div>

      <button className="btn" onClick={runCopywriter}>
        Run Copywriter Agent
      </button>
    </div>
  )
}

export default CopywriterPanel

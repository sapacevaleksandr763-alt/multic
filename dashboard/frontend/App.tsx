import React, { useState, useEffect } from 'react'
import './App.css'
import ScoutPanel from './pages/ScoutPanel'
import CopywriterPanel from './pages/CopywriterPanel'
import PromotionPanel from './pages/PromotionPanel'
import AnalyticsPanel from './pages/AnalyticsPanel'
import VideoTimeline from './components/VideoTimeline'
import PlatformChart from './components/PlatformChart'
import SystemLogs from './components/SystemLogs'

interface DashboardData {
  scout: {
    videos_found_today: number
    total_videos: number
    engagement_ratio_avg: number
    last_search: string
    status: string
  }
  copywriter: {
    videos_analyzing: number
    variants_generated: number
    status: string
  }
  promotion: {
    videos_published: number
    platforms_active: number
    total_views: number
    status: string
  }
  analytics: {
    youtube_views: number
    telegram_views: number
    vk_views: number
    instagram_views: number
    avg_engagement: number
  }
}

const App: React.FC = () => {
  const [data, setData] = useState<DashboardData>({
    scout: {
      videos_found_today: 0,
      total_videos: 0,
      engagement_ratio_avg: 0,
      last_search: '',
      status: 'initializing',
    },
    copywriter: {
      videos_analyzing: 0,
      variants_generated: 0,
      status: 'idle',
    },
    promotion: {
      videos_published: 0,
      platforms_active: 0,
      total_views: 0,
      status: 'ready',
    },
    analytics: {
      youtube_views: 0,
      telegram_views: 0,
      vk_views: 0,
      instagram_views: 0,
      avg_engagement: 0,
    },
  })

  const [activeTab, setActiveTab] = useState<'overview' | 'timeline' | 'charts' | 'logs'>('overview')

  useEffect(() => {
    // Загружаем данные с backend при монтировании
    fetchDashboardData()

    // WebSocket для real-time обновлений
    const ws = new WebSocket('ws://localhost:8000/ws/dashboard')
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data)
      setData((prev) => ({ ...prev, ...update }))
    }

    return () => ws.close()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard')
      const dashboardData = await response.json()
      setData(dashboardData)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎬 MULTIC MASTER DASHBOARD</h1>
        <p>Real-time System Monitor</p>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`nav-btn ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => setActiveTab('timeline')}
        >
          Video Timeline
        </button>
        <button
          className={`nav-btn ${activeTab === 'charts' ? 'active' : ''}`}
          onClick={() => setActiveTab('charts')}
        >
          Analytics
        </button>
        <button
          className={`nav-btn ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          System Logs
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'overview' && (
          <div className="overview-grid">
            <ScoutPanel data={data.scout} />
            <CopywriterPanel data={data.copywriter} />
            <PromotionPanel data={data.promotion} />
            <AnalyticsPanel data={data.analytics} />
          </div>
        )}

        {activeTab === 'timeline' && <VideoTimeline />}

        {activeTab === 'charts' && (
          <div className="charts-container">
            <PlatformChart data={data.analytics} />
          </div>
        )}

        {activeTab === 'logs' && <SystemLogs />}
      </main>

      <footer className="app-footer">
        <p>MULTIC System | Last updated: {new Date().toLocaleTimeString()}</p>
      </footer>
    </div>
  )
}

export default App

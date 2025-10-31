import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './styles/index.css'

// App 부트스트랩: React 루트 마운트, BrowserRouter 활성화, 전역 스타일 로드
// 로딩 두 번씩 돼서 StrictMode 삭제함
createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)

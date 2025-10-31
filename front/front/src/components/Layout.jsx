import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useTrip } from '../hooks/useTrip'
import { useState, useEffect } from 'react'
import Popover from './Popover'
import dayjs from 'dayjs'
import { getWeather, getTripWeatherMessages } from '../services/weatherService'
import Button from './ui/Button'

// 앱 크롬(사이드바 + 상단바)과 로그아웃 동작 담당
export default function Layout(){
  const loc = useLocation()
  const nav = useNavigate()
  const [user, setUser] = useState(null)
  const [openBell, setOpenBell] = useState(false)
  const { getCurrentUser, logout } = useAuth()

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const userData = await getCurrentUser()
          setUser(userData)
        } catch (err) {
          console.error('사용자 정보 조회 실패:', err)
        }
      }
    }
    fetchUser()
  }, [loc.pathname])
  return (
    <div className="grid h-screen overflow-hidden" style={{gridTemplateColumns: '280px 1fr'}}>
      <aside className="px-5 py-6 bg-gradient-sidebar backdrop-blur border-r border-primary-dark/12 relative overflow-hidden">
        <div className="font-bold text-2xl tracking-tight mb-8 text-sidebar-brand" style={{filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.08))'}}>Plan‑it</div>
        <nav className="flex flex-col gap-2">
          <NavLink to="/" className={({isActive})=> isActive
            ? 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-semibold text-white shadow-button bg-gradient-primary'
            : 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-medium text-sidebar-link hover:bg-emerald-500/15 hover:translate-x-1'}>
            <span className="w-5 text-center text-lg" aria-hidden>🏠</span>
            <span>대시보드</span>
          </NavLink>
          <NavLink to="/trips" className={({isActive})=> isActive
            ? 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-semibold text-white shadow-button bg-gradient-primary'
            : 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-medium text-sidebar-link hover:bg-emerald-500/15 hover:translate-x-1'}>
            <span className="w-5 text-center text-lg" aria-hidden>🧳</span>
            <span>여행</span>
          </NavLink>
          <NavLink to="/community" className={({isActive})=> isActive
            ? 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-semibold text-white shadow-button bg-gradient-primary'
            : 'no-underline px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden flex gap-3 items-center font-medium text-sidebar-link hover:bg-emerald-500/15 hover:translate-x-1'}>
            <span className="w-5 text-center text-lg" aria-hidden>🗣️</span>
            <span>커뮤니티</span>
          </NavLink>
        </nav>
      </aside>
      <div className="flex flex-col h-screen overflow-hidden">
        <div className="bg-surface rounded-t-3xl mx-6 p-5 pb-6 backdrop-blur border border-primary-dark/12 relative">
          <header className="flex gap-4 items-center py-5 px-6 bg-bg-card backdrop-blur border-b border-primary-dark/15 sticky top-0 z-10">
            <div className="flex items-center gap-3 flex-1 min-w-[420px]">
              <input className="flex-1 h-13 px-5 rounded-[26px] bg-white text-text border border-primary-dark/20 text-sm transition focus:outline-none focus:border-primary focus:shadow-[0_0_0_3px_rgba(16,185,129,0.12)] placeholder:text-text-soft" placeholder="Search for your favourite destination" />
              <button className="h-13 px-6 rounded-[26px] bg-gradient-primary text-white font-semibold cursor-pointer text-sm transition shadow-button hover:-translate-y-px hover:shadow-lg">Search</button>
            </div>
            <div className="ml-auto flex gap-3 items-center">
              <button className="bell bg-surface border border-primary-dark/15 rounded-xl w-12 h-12 grid place-items-center cursor-pointer text-text transition hover:bg-emerald-50 hover:-translate-y-px" title="알림" onClick={()=>setOpenBell(v=>!v)}>🔔</button>
              <Popover open={openBell} onClose={()=>setOpenBell(false)} anchorClass=".bell">
                <BellContent />
              </Popover>
              {user ? (
                <div className="flex gap-3 items-center">
                  <div className="w-10 h-10 rounded-full bg-gradient-primary grid place-items-center font-semibold text-white cursor-pointer transition border-2 border-emerald-500/20 hover:scale-105" onClick={()=>nav('/profile')}>{user.username?.[0]?.toUpperCase()||user.email?.[0]?.toUpperCase()||'U'}</div>
                  <div className="flex flex-col leading-tight">
                    <div className="font-semibold text-text">{user.username || user.email || 'User'}</div>
                  </div>
                  <Button variant="inverse" onClick={()=>{ logout(); nav('/login') }}>로그아웃</Button>
                </div>
              ) : (
                <Button onClick={()=>nav('/login')}>로그인</Button>
              )}
            </div>
          </header>
          <Outlet key={loc.key} />
        </div>
      </div>
    </div>
  )
}

// 여행 일정과 날씨 정보를 합쳐 알림 목록 생성
// 여행 일정과 날씨 정보를 합쳐 알림 목록 생성
function BellContent() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [nextTrip, setNextTrip] = useState(null) // ✅ 추가
  const { getNextTrip } = useTrip()
  const { getCurrentUser } = useAuth()

  
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        setLoading(true)
        const user = await getCurrentUser()
        if (!user) {
          setItems([{ text: '로그인이 필요합니다.', head: true }])
          return
        }

        const trip = await getNextTrip(user.id)
        setNextTrip(trip) // ✅ 저장

        if (!trip) {
          setItems([{ text: '다가오는 여행이 없습니다.', head: true }])
          return
        }

        const now = dayjs()
        const startDate = dayjs(trip.start_date)
        const endDate = dayjs(trip.end_date)
        const diff = startDate.diff(now, 'day')

        console.log('🎯 trip 데이터:', trip)
        console.log('🕒 diff:', diff)
        console.log('🌐 lat/lon:', trip.lat, trip.lon)
        
        let notifications = [
          { text: '🌤️ 여행 알림', head: true },
          { text: `✈️ "${trip.title}" 여행 D-${diff}` },
        ]

        if (diff <= 4 && diff >= 0 && trip.city_name) {
          const weatherMessages = await getTripWeatherMessages({
            city_name: trip.city_name,
            lat: trip.lat,
            lon: trip.lon,
            start_date: startDate.format('YYYY-MM-DD'),
            end_date: endDate.format('YYYY-MM-DD'),
            diffDays: diff,
          })

          console.log('🌦️ 날씨 메시지:', weatherMessages)
          if (weatherMessages && weatherMessages.length > 0) {
            weatherMessages.forEach((m) => {
              notifications.push({ text: m })
            })
          } else {
            notifications.push({ text: '❌ 표시할 날씨 예보가 없습니다.' })
          }
        }

        setItems(notifications)
      } catch (err) {
        console.error('알림 조회 실패:', err)
        setItems([{ text: '알림 불러오기 실패', head: true }])
      } finally {
        setLoading(false)
      }
    }

    fetchNotifications()
  }, [])

  if (loading) {
    return (
      <div className="text-sm text-text-soft p-3">
        ☁️ 알림 불러오는 중...
      </div>
    )
  }

  return (
    <div>
      {items.map((n, i) =>
        n.head ? (
          <div
            key={i}
            className="text-sm font-medium text-text-soft mb-2 flex items-center gap-2"
          >
            {n.text}
          </div>
        ) : (
          <div
            key={i}
            className="p-3 rounded-xl bg-surface mb-2 last:mb-0 border border-primary-dark/10 text-sm"
          >
            {n.text}
          </div>
        )
      )}
    </div>
  )
}

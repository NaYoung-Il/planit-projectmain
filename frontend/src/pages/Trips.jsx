import { Link } from 'react-router-dom'
import Card from '../components/Card'
import { useEffect, useState } from 'react'
import { useTrip } from '../hooks/useTrip'
import { useAuth } from '../hooks/useAuth'
import Button from '../components/ui/Button'
import Empty from '../components/ui/Empty'

// Trips : 저장된 여행 목록 표시 및 수정 화면 이동
export default function Trips(){
  const [items, setItems] = useState([])
  const { getTripsByUser, deleteTrip, loading } = useTrip()
  const { getCurrentUser } = useAuth()

  useEffect(()=>{
    const fetchTrips = async () => {
      try {
        const user = await getCurrentUser()
        // 1. 이 API 호출 한 번으로 모든 정보 (Trip + TripCities + City)를 가져옵니다.
        const trips = await getTripsByUser(user.id)

        // 2. 프론트엔드에서 도시 이름만 추출합니다.
        const tripsWithCity = trips.map((trip) => {
          let cityName = ''
          // trip_cities 배열이 있고, 비어있지 않다면
          if (trip.trip_cities && trip.trip_cities.length > 0) {
            // 첫 번째 도시의 한글 이름을 사용합니다.
            cityName = trip.trip_cities[0]?.city?.ko_name || '도시 정보 없음' 
          }
          return { ...trip, city_name: cityName }
        })

        setItems(tripsWithCity)
      } catch (err) {
        console.error('여행 목록 조회 실패:', err)
      }
    }
    fetchTrips()
  }, [])

  const del = async (id) => {
    try {
      if (!window.confirm('정말 삭제하시겠습니까?')) return // ⬅️ (추가) 확인창

      await deleteTrip(id)
      
      // ⬇️ [수정] 삭제 성공 시, API를 다시 호출하여 목록을 갱신합니다.
      //    (N+1 로직을 재사용할 필요 없음)
      fetchTrips() 

    } catch (err) {
      alert('여행 삭제에 실패했습니다')
    }
  }

  return (
    <Card className='m-6' title="여행" right={<Link to="/trips/new"><Button>+ 새 여행</Button></Link>}>
      <div className="flex flex-col gap-3">
        {loading && <div className="text-center text-text-soft">로딩 중...</div>}
        {!loading && items.length===0 && <Empty message="아직 여행이 없어요. 새 여행을 추가해보세요." />}
        {!loading && items.map(t=> (
          <Link key={t.id} to={`/trips/${t.id}`} className="block">
            <div className="p-4 rounded-lg border border-primary-dark/15 flex items-center justify-between gap-2 bg-white/55 backdrop-blur shadow-card hover:shadow-lg hover:border-primary-dark/30 transition-all cursor-pointer">
              <div>
                <h4 className="text-base font-semibold text-text m-0">{t.title || t.name}</h4>
                <div className="text-xs text-text-soft flex gap-3 mt-1">{t.city_name} · {(t.start_date || t.start).split('T')[0]} ~ {(t.end_date || t.end).split('T')[0]}</div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </Card>
  )
}

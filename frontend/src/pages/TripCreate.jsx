import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import Card from '../components/Card'
import { useTrip } from '../hooks/useTrip'
import { useAuth } from '../hooks/useAuth'
import { useCity } from '../hooks/useCity'
import dayjs from 'dayjs'
import TripCreate1 from './TripCreate1'
import TripCreate2 from './TripCreate2'
import TripCreate3 from './TripCreate3'

// TripCreate : 단계별 여행 생성 페이지 (메인 컨트롤러)
export default function TripCreate() {
  const nav = useNavigate()
  const location = useLocation()

  const [step, setStep] = useState(1)

  // 기본 정보
  const [tripName, setTripName] = useState('')
  const [country, setCountry] = useState('')
  const [startDate, setStartDate] = useState(location.state?.start_date || '')
  const [endDate, setEndDate] = useState(location.state?.end_date || '')

  // 도시별 일정 (city: city_name 영문명, ko_name: 한글명)
  const [citySchedules, setCitySchedules] = useState([
    { id: crypto.randomUUID(), city: '', ko_name: '', startDate: '', endDate: '' }
  ])

  // Step 3: 일자별 상세 일정
  const [dayDetails, setDayDetails] = useState({})
  const [expandedDay, setExpandedDay] = useState(null)

  // 여행별 체크리스트
  const [checklists, setChecklists] = useState([])

  const {
    createTrip,
    createTripDay,
    createSchedule,
    createChecklistItem,
    getTripDays,
    loading
  } = useTrip()
  const { getCurrentUser } = useAuth()
  const { getCityByName } = useCity()

  // 일자별 목록 생성
  const getDaysList = () => {
    const days = []
    citySchedules.forEach(schedule => {
      if (schedule.startDate && schedule.endDate && schedule.city) {
        let current = dayjs(schedule.startDate)
        const end = dayjs(schedule.endDate)
        while (current.isBefore(end) || current.isSame(end, 'day')) {
          days.push({
            date: current.format('YYYY-MM-DD'),
            city: schedule.ko_name, // 한글명 출력
            dayNumber: days.length + 1
          })
          current = current.add(1, 'day')
        }
      }
    })
    return days
  }

  // 체크리스트 추가 (여행별)
  const addCheck = () => {
    setChecklists([
      ...checklists,
      { id: crypto.randomUUID(), is_checked: false, item_name: '' }
    ])
  }

  // 체크리스트 업데이트 (여행별)
  const handleUpdateCheck = (itemId, field, value) => {
    setChecklists(checklists.map(item =>
      item.id === itemId ? { ...item, [field]: value } : item
    ))
  }

  // 체크리스트 삭제 (여행별)
  const handleRemoveCheck = (itemId) => {
    setChecklists(checklists.filter(item => item.id !== itemId))
  }

  // 일정 추가
  const addSchedule = (date) => {
    setDayDetails(prev => ({
      ...prev,
      [date]: {
        ...prev[date],
        schedules: [
          ...(prev[date]?.schedules || []),
          { id: crypto.randomUUID(), schedule_content: '', start_time: '', end_time: '', place: '' }
        ]
      }
    }))
  }

  // 일정 업데이트
  const handleUpdateSchedule = (date, itemId, field, value) => {
    setDayDetails(prev => ({
      ...prev,
      [date]: {
        ...prev[date],
        schedules: (prev[date]?.schedules || []).map(item =>
          item.id === itemId ? { ...item, [field]: value } : item
        )
      }
    }))
  }

  // 일정 삭제
  const handleRemoveSchedule = (date, itemId) => {
    setDayDetails(prev => ({
      ...prev,
      [date]: {
        ...prev[date],
        schedules: (prev[date]?.schedules || []).filter(item => item.id !== itemId)
      }
    }))
  }

  // 11/2 수정(나영일) : 여행 생성 최종 제출
  const handleSubmit = async () => {
    try {
      const user = await getCurrentUser()
      
      const tripCities = citySchedules.map(cs => ({
        start_date: cs.startDate,
        end_date: cs.endDate,
        city_id: cs.city_id,
      }));

      const trip = {
        title: tripName,
        start_date: startDate,
        end_date: endDate,
        user_id: user.id,
        trip_cities: tripCities,
      }

      // 여행 정보 생성
      const newTrip = await createTrip(trip);
      const newTripId = newTrip.id;

      // 11/2 수정(나영일) : 백엔드가 생성한 '새 TripDay' 목록을 가져옴
      const newTripDays = await getTripDays(newTripId);
      const dayIdMap = new Map();
      newTripDays.forEach(td => {
        dayIdMap.set(td.day_sequence, td.id);
      });
      

      // 체크리스트 항목 저장 (여행별)
      for (const item of checklists) {
        if (item.item_name.trim()) {
          await createChecklistItem({
            trip_id: newTripId,
            item_name: item.item_name,
            is_checked: item.is_checked
          })
        }
      }

      const daysList = getDaysList();

      // 일자별 상세 정보 저장
      for (const day of daysList) {
        // 일자별 여행 계획 생성
        const sequence = day.dayNumber;
        const currentTripDayId = dayIdMap.get(sequence);
        if (currentTripDayId) {
          const schedules = dayDetails[day.date]?.schedules || []
          // 세부 일정 저장
          for (const schedule of schedules) {
            if (schedule.schedule_content.trim()) {
              await createSchedule({
                trip_day_id: currentTripDayId,
                schedule_content: schedule.schedule_content,
                start_time: schedule.start_time || null,
                end_time: schedule.end_time || null,
                place_id: null,
                schedule_datetime: new Date().toISOString()
              })
            }
          }
        }
      }

      nav('/trips')
    } catch (err) {
      console.error('여행 생성 실패:', err);
      // 422 에러의 상세 내용을 보여줌
      const errorDetail = err.response?.data?.detail;
      if (errorDetail) {
        alert('여행 생성 실패: ' + JSON.stringify(errorDetail));
      } else {
        alert('여행 생성에 실패했습니다: ' + err.message);
      }
    } 
  }

  return (
    <Card title="새 여행" className="m-6">
      {step === 1 && (
        <TripCreate1
          tripName={tripName}
          setTripName={setTripName}
          country={country}
          setCountry={setCountry}
          startDate={startDate}
          setStartDate={setStartDate}
          endDate={endDate}
          setEndDate={setEndDate}
          onNext={() => setStep(2)}
        />
      )}

      {step === 2 && (
        <TripCreate2
          country={country}
          startDate={startDate}
          endDate={endDate}
          citySchedules={citySchedules}
          setCitySchedules={setCitySchedules}
          onNext={() => setStep(3)}
          onPrevious={() => setStep(1)}
        />
      )}

      {step === 3 && (
        <TripCreate3
          daysList={getDaysList()}
          dayDetails={dayDetails}
          expandedDay={expandedDay}
          setExpandedDay={setExpandedDay}
          checklists={checklists}
          onAddCheck={addCheck}
          onUpdateCheck={handleUpdateCheck}
          onRemoveCheck={handleRemoveCheck}
          onAddSchedule={addSchedule}
          onUpdateSchedule={handleUpdateSchedule}
          onRemoveSchedule={handleRemoveSchedule}
          onSubmit={handleSubmit}
          onPrevious={() => setStep(2)}
          loading={loading}
        />
      )}
    </Card>
  )
}

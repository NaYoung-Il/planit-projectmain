import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import Card from '../components/Card'
import Button from '../components/ui/Button'
import FormField from '../components/ui/FormField'
import Separator from '../components/ui/Separator'
import { useTrip } from '../hooks/useTrip'
import { useCity } from '../hooks/useCity'
import { useAuth } from '../hooks/useAuth'
import dayjs from 'dayjs'
import isBetween from 'dayjs/plugin/isBetween'

dayjs.extend(isBetween)

export default function TripInfoEdit() {
  const nav = useNavigate()
  const { id } = useParams()
  const [isEditMode, setIsEditMode] = useState(false)
  const [isLoadingData, setIsLoadingData] = useState(true)
  const [hasResetWarningShown, setHasResetWarningShown] = useState(false)

  // Step 1: 기본 정보
  const [tripName, setTripName] = useState('')
  const [country, setCountry] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  // 나라/도시 목록
  const [countries, setCountries] = useState([])
  const [cities, setCities] = useState([])

  // Step 2: 도시별 일정 
  const [citySchedules, setCitySchedules] = useState([
    { id: crypto.randomUUID(), city: '', ko_name: '', startDate: '', endDate: '' }
  ])

  // Step 3: 일자별 상세 일정
  const [dayDetails, setDayDetails] = useState({})
  const [expandedDay, setExpandedDay] = useState(null)
  const [tripDays, setTripDays] = useState([])

  // 여행별 체크리스트
  const [checklists, setChecklists] = useState([])

  // 11/2 추가(나영일) : 삭제할 항목의 ID를 임시 저장할 State
  const [checklistsToDelete, setChecklistsToDelete] = useState([])
  const [schedulesToDelete, setSchedulesToDelete] = useState([])

  // 원본 데이터 보관 (변경 감지용)
  const [originalData, setOriginalData] = useState({
    startDate: '',
    endDate: '',
    citySchedules: []
  })

  const {
    getTrip,
    getTripCitiesByTripId, // 11/2 수정 : useTrip 훅에 추가
    getTripDays,
    getSchedulesByDay,
    getChecklistItemsByTrip,
    updateTrip,
    deleteTrip,
    createTripDay,
    createSchedule,
    createChecklistItem,
    updateSchedule,
    updateChecklistItem,
    deleteSchedule,
    deleteChecklistItem,
    loading
  } = useTrip()
  const { getCity, getAllCities } = useCity()
  const { getCurrentUser } = useAuth()

  // 나라/도시 목록 로드
  useEffect(() => {
    const fetchCitiesData = async () => {
      const allCities = await getAllCities()
      // ko_country 필드에서 중복 제거 후 정렬
      const countryList = [...new Set(allCities.map(city => city.ko_country).filter(Boolean))].sort()
      setCountries(countryList)
    }
    fetchCitiesData()
  }, [])

  // 선택된 나라에 따라 도시 목록 필터링
  useEffect(() => {
    const fetchFilteredCities = async () => {
      if (country) {
        const allCities = await getAllCities()
        // ko_country와 일치하는 도시만 필터링
        const filteredCities = allCities.filter(city => city.ko_country === country)
        setCities(filteredCities)
      }
    }
    fetchFilteredCities()
  }, [country])

  // 데이터 로드
  useEffect(() => {
    loadTripData()
  }, [id])

  // 11/2 수정(나영일) : trip.city_id 대신 trip_id에 연결된 trip_cities 목록을 가져오도록 변경
  const loadTripData = async () => {
    try {
      setIsLoadingData(true)

      const trip = await getTrip(id)
      setTripName(trip.title)
      setStartDate(trip.start_date?.split('T')[0])
      setEndDate(trip.end_date?.split('T')[0])

      const fetchedTripDays = await getTripDays(id)
      setTripDays(fetchedTripDays)

      // 수정 : city_id 대신 trip_cities 목록을 가져옴
      const fetchedTripCities = await getTripCitiesByTripId(id)

      // 수정 : fetchedTripCities (배열)을 기반으로 citySchedules 상태 복원
      const restoredCitySchedules = fetchedTripCities.map(tc => {
        // 백엔드 API가 tc.city 객체를 포함(join)해서 보내준다고 가정
        return {
          id: tc.id, // DB의 실제 ID (crypto.randomUUID() 대신)
          city: tc.city.city_name, // 영문명
          city_id: tc.city.id,     // City의 ID
          ko_name: tc.city.ko_name,  // 한글명
          startDate: tc.start_date,
          endDate: tc.end_date
        }
      })
      
      setCitySchedules(restoredCitySchedules.length > 0 ? restoredCitySchedules 
        : [{ id: crypto.randomUUID(), city: '', ko_name: '', 
          startDate: '', endDate: '' }])

      // 수정 : Country 정보는 첫 번째 도시를 기준으로 설정
      if (fetchedTripCities.length > 0) {
        setCountry(fetchedTripCities[0].city.ko_country)
      }

      // 원본 데이터 저장
      setOriginalData({
        startDate: trip.start_date,
        endDate: trip.end_date,
        citySchedules: JSON.parse(JSON.stringify(restoredCitySchedules))
      })

      // 체크리스트 조회
      const fetchedChecklists = await getChecklistItemsByTrip(id)
      setChecklists(fetchedChecklists.map(item => ({
        ...item,
        id: item.id || crypto.randomUUID(),
        isNew: false
      })))

      // 일자별 일정 조회 
      // 11/2 수정(나영일) : Key를 day_date -> day_sequence로 변경
      const allDayDetails = {}
      for (const tripDay of fetchedTripDays) {
        const sequence = tripDay.day_sequence
        const schedules = await getSchedulesByDay(tripDay.id)

        allDayDetails[sequence] = {
          tripDayId: tripDay.id,
          schedules: schedules.map(schedule => ({
            ...schedule,
            id: schedule.id || crypto.randomUUID(),
            start_time: schedule.start_time,
            end_time: schedule.end_time,
            place: schedule.place_id ?? '',
            isNew: false
          }))
        }
      }
      setDayDetails(allDayDetails);
    } catch (err) {
      console.error('여행 데이터 로드 실패:', err)
      alert('여행 데이터를 불러오는데 실패했습니다.')
      nav('/trips')
    } finally {
      setIsLoadingData(false)
    }
  }

  // 일자별 목록 생성
  // 11/2 수정(나영일) : 날짜를 동적으로 계산
  const getDaysList = () => {
    if (!startDate || !endDate) return [];

    const days = [];
    let current = dayjs(startDate);
    const end = dayjs(endDate);
    let dayNumber = 1;

    while (current.isBefore(end) || current.isSame(end, 'day')) {
      const dateStr = current.format('YYYY-MM-DD');
      
      // 개선 : 이 날짜가 어떤 도시에 속하는지 찾기
      const citySchedule = citySchedules.find(cs => 
        dayjs(dateStr).isBetween(cs.startDate, cs.endDate, 'day', '[]')
      );

      days.push({
        date: dateStr, // 동적으로 계산된 실제 날짜
        city: citySchedule?.ko_name || '도시 미정',
        dayNumber: dayNumber // 1, 2, 3...
      });
      
      current = current.add(1, 'day');
      dayNumber++;
    }
    return days;
  };

  // 11/2 수정(나영일) : 일정 초기화 확인 로직 삭제

  // Step 1 핸들러
  const handleStartDateChange = (e) => {
    setStartDate(e.target.value)
  }

  const handleEndDateChange = (e) => {
    setEndDate(e.target.value)
  }

  // Step 2 핸들러
  const addCitySchedule = () => {
    setCitySchedules([...citySchedules, {
      id: crypto.randomUUID(),
      city: '',
      city_id: null, // 추가
      ko_name: '',
      startDate: '',
      endDate: ''
    }])
  }

  const removeCitySchedule = (id) => {
    setCitySchedules(citySchedules.filter(s => s.id !== id))
    if (checkAndResetSchedule('citySchedule')) {
      // 초기화 진행
    }
  }

  // 11/2 수정(나영일) : city를 선택할 때 city_id도 함께 state에 저장하도록 변경
  const updateCitySchedule = (id, field, value) => {

    // 수정 : 도시 선택 시 city_id와 ko_name을 함께 저장
    if (field === 'city') {
      const selectedCity = cities.find(c => c.city_name === value)
      setCitySchedules(citySchedules.map(s =>
        s.id === id 
          ? { ...s, city: value, city_id: selectedCity?.id, ko_name: selectedCity?.ko_name } 
          : s
      ))
    } else {
      setCitySchedules(citySchedules.map(s =>
        s.id === id ? { ...s, [field]: value } : s
      ))
    }
  }

  // Step 3 핸들러
  // 체크리스트 추가
  const addCheck = () => {
    setChecklists([
      ...checklists,
      { id: crypto.randomUUID(), is_checked: false, item_name: '', isNew: true }
    ])
  }

  // 체크리스트 업데이트
  const handleUpdateCheck = async (itemId, field, value) => {
    // 로컬 상태 업데이트
    setChecklists(checklists.map(item =>
      item.id === itemId ? { ...item, [field]: value } : item
    ))

    // is_checked 변경되면 바로 DB 저장
    if (field === 'is_checked') {
        const item = checklists.find(c => c.id === itemId)
        if (item && !item.isNew) {
          await updateChecklistItem(itemId, {
            item_name: item.item_name,
            is_checked: value
          })
        }
    }
  }

  // 체크리스트 삭제
  const handleRemoveCheck = (itemId) => {
    // 11/2 수정 : 삭제할 항목이 'isNew' (새 항목)가 아닌지 확인
    const itemToRemove = checklists.find(item => item.id === itemId);
    if (itemToRemove && !itemToRemove.isNew) {
      // DB에 저장된 항목이면 '삭제 목록'에 ID 추가
      setChecklistsToDelete(prev => [...prev, itemId]);
    }
    setChecklists(checklists.filter(item => item.id !== itemId))
  }

  const addSchedule = (dayNumber) => {
    setDayDetails(prev => ({
      ...prev,
      [dayNumber]: {
        ...prev[dayNumber],
        schedules: [
          ...(prev[dayNumber]?.schedules || []),
          { id: crypto.randomUUID(), schedule_content: '', start_time: '', end_time: '', place: '', isNew: true }
        ]
      }
    }))
  }

  const handleUpdateSchedule = (dayNumber, itemId, field, value) => {
    setDayDetails(prev => ({
      ...prev,
      [dayNumber]: {
        ...prev[dayNumber],
        schedules: (prev[dayNumber]?.schedules || []).map(item =>
          item.id === itemId ? { ...item, [field]: value } : item
        )
      }
    }))
  }

  const handleRemoveSchedule = (dayNumber, itemId) => {
    // 수정 : 삭제할 항목 찾기
    const itemToRemove = dayDetails[dayNumber]?.schedules.find(item => item.id === itemId);
    if (itemToRemove && !itemToRemove.isNew) {
      // DB에 저장된 항목이면 '삭제 목록'에 ID 추가
      setSchedulesToDelete(prev => [...prev, itemId]);
    }
    setDayDetails(prev => ({
      ...prev,
      [dayNumber]: {
        ...prev[dayNumber],
        schedules: (prev[dayNumber]?.schedules || []).filter(item => item.id !== itemId)
      }
    }))
  }

  // 삭제
  const handleDelete = async () => {
    if (!window.confirm('정말 삭제하시겠습니까?')) return

    try {
      await deleteTrip(id)
      alert('여행이 삭제되었습니다.')
      nav('/trips')
    } catch (err) {
      console.error('여행 삭제 실패:', err)
      alert('여행 삭제에 실패했습니다.')
    }
  }

  // 11/2 수정(나영일) : 여행 수정 제출 핸들러
  // TripDay와 Schedule을 수동으로 삭제/생성하는 모든 코드 제거
  const handleSubmit = async () => {
    try {
      const user = await getCurrentUser()
      
      // 삭제할 Schedule과 ChecklistItem 처리
      if (schedulesToDelete.length > 0) {
        await Promise.all(schedulesToDelete.map(id => deleteSchedule(id)));
        setSchedulesToDelete([]); // 삭제 목록 비우기
      }
      if (checklistsToDelete.length > 0) {
        await Promise.all(checklistsToDelete.map(id => deleteChecklistItem(id)));
        setChecklistsToDelete([]); // 삭제 목록 비우기
      }

      const tripCitiesPayload = citySchedules.map(cs => ({
        city_id: cs.city_id,
        start_date: cs.startDate,
        end_date: cs.endDate
      }))
      
      // 유효성 검사 로직 -> 모든 도시가 선택되었는지 확인 (city_id가 null/undefined가 아닌지)
      const hasInvalidCity = tripCitiesPayload.some(city => !city.city_id);
      if (hasInvalidCity) {
        alert('모든 도시별 일정에 도시를 선택해주세요.');
        return; // 전송 중단
      }

      const tripUpdatePayload = {
        title: tripName,
        start_date: startDate,
        end_date: endDate,
        trip_cities: tripCitiesPayload, // 검증된 배열 사용
      }

      // 수정 : 백엔드 API 한 번 호출로 Trip, TripCity, TripDay 모두 업데이트
      // 백엔드 update_trip 서비스가 모든 로직을 처리
      await updateTrip(id, tripUpdatePayload)

      // 백엔드에서 TripDay가 변경되었을 수 있으니, 최신 데이터를 다시 불러옴
      const newTripDays = await getTripDays(id);
      const dayIdMap = new Map(); // key: day_sequence, value: trip_day.id
      newTripDays.forEach(td => {
        dayIdMap.set(td.day_sequence, td.id);
      })

      // 수정 : hasDateOrCityChanged 로직 삭제, if-else 없이 모두 처리
      // 체크리스트 수정
      for (const item of checklists) {
        if (item.isNew) {
          if (item.item_name.trim()) {
            await createChecklistItem({
              trip_id: parseInt(id),
              item_name: item.item_name,
              is_checked: item.is_checked
            })
          }
        } else {
          await updateChecklistItem(item.id, {
            item_name: item.item_name,
            is_checked: item.is_checked
          })
        }
      }

      // 스케줄만 수정
      
      const daysList = getDaysList();

      for (const day of daysList) {
        const sequence = day.dayNumber;
        const details = dayDetails[sequence]; // 프론트 state에서 일정 가져오기

        // 백엔드에서 최신 trip_day.id 가져오기
        const currentTripDayId = dayIdMap.get(sequence);

        if (!currentTripDayId) continue; // 축소되어 삭제된 날

        // 스케줄
        for (const schedule of details?.schedules || []) {
          if (schedule.isNew) {
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
          } else {
            await updateSchedule(schedule.id, {
              schedule_content: schedule.schedule_content,
              start_time: schedule.start_time || null,
              end_time: schedule.end_time || null,
              place_id: null
            })
          }
        }
      }
      //    (참고) 삭제된 Schedule은 어떻게 처리?
      //    프론트에서 handleRemoveSchedule 시 state에서만 지우고,
      //    handleSubmit에서 '삭제 목록'을 따로 관리했다가
      //    deleteSchedule(id)를 호출해야 합니다.
      //    (현재 코드는 삭제 로직이 handleSubmit에 없음)
      alert('여행이 수정되었습니다.')
      setIsEditMode(false)
      await loadTripData();
    } catch (err) {
      console.error('여행 수정 실패:', err)
      const errorDetail = err.response?.data?.detail;
      if (errorDetail) {
        alert('여행 수정 실패 (422): ' + JSON.stringify(errorDetail));
      } else {
        alert('여행 수정에 실패했습니다: ' + err.message);
      }
    }
  }

  if (isLoadingData) {
    return (
      <Card title="여행 정보" subtitle="여행 정보">
        <div className="flex justify-center items-center py-8">
          <p className="text-text-soft">데이터를 불러오는 중...</p>
        </div>
      </Card>
    )
  }

  return (
    <Card
      className="m-6"
      title={tripName}
      subtitle={isEditMode ? '여행 수정' : '여행 정보'}
      right={
        <div className="flex gap-2">
          {!isEditMode ? (
            <>
              <Button onClick={() => setIsEditMode(true)}>수정</Button>
              <button
                onClick={handleDelete}
                className="text-lg hover:scale-110 transition-transform"
                title="삭제"
              >
                🗑️
              </button>
            </>
          ) : (
            <Button onClick={handleSubmit} disabled={loading}>
              {loading ? '저장 중...' : '수정 완료'}
            </Button>
          )}
        </div>
      }
    >
      <div className="flex flex-col gap-6">
        {/* Step 1: 기본 정보 */}
        <div>
          {!isEditMode ? (
            <div className="flex flex-col gap-3">
              <div>
                <span className="text-lg font-bold text-text-soft">🚩 COUNTRY</span>
                <p className="text-text text-lg mt-1">{country}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-lg font-bold text-text-soft">🛫 START</span>
                  <p className="text-text text-lg mt-1">{startDate?.split('T')[0]}</p>
                </div>
                <div>
                  <span className="text-lg font-bold text-text-soft">🛬 END</span>
                  <p className="text-text text-lg mt-1">{endDate?.split('T')[0]}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              <FormField
                label="여행 이름"
                value={tripName}
                onChange={e => setTripName(e.target.value)}
                required
                placeholder="예: 일본 여행"
              />
              <div>
                <label className="block text-sm font-semibold text-text mb-2">나라 *</label>
                <input
                  type="text"
                  value={country}
                  disabled
                  className="w-full px-4 py-2.5 rounded-lg border border-primary-dark/20 bg-gray-100 text-text-soft text-sm cursor-not-allowed"
                  title="나라 변경은 지원되지 않습니다. 새 여행을 생성해주세요."
                />
                <p className="text-xs text-text-soft mt-1">나라 변경은 지원되지 않습니다. 새 여행을 생성해주세요.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  label="출발일"
                  type="date"
                  value={startDate?.split('T')[0]}
                  onChange={handleStartDateChange}
                  required
                />
                <FormField
                  label="도착일"
                  type="date"
                  value={endDate?.split('T')[0]}
                  onChange={handleEndDateChange}
                  required
                  min={startDate?.split('T')[0]}
                />
              </div>
            </div>
          )}
        </div>

        <Separator />

        {/* Step 2: 도시 선택 */}
        <div>
          <h3 className="text-lg font-semibold text-text mb-4">📍 도시별 일정</h3>
          {!isEditMode ? (
            <div className="flex flex-col gap-2">
              {citySchedules.map((schedule, index) => (
                <div key={schedule.id} className="text-text">
                  <span className="font-semibold">{schedule.ko_name}</span>
                  <span className="text-text-soft text-sm ml-2">
                    {schedule.startDate?.split('T')[0]} ~ {schedule.endDate?.split('T')[0]}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <>
              <div className="text-sm text-text-soft mb-4">
                총 여행 기간: {dayjs(endDate).diff(dayjs(startDate), 'day') + 1}일
              </div>
              {citySchedules.map((schedule, index) => (
                <div key={schedule.id} className="p-4 border border-primary-dark/20 rounded-lg bg-white/50 mb-3">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-sm font-semibold text-text">도시 {index + 1}</span>
                    {index > 0 && (
                      <button
                        type="button"
                        onClick={() => removeCitySchedule(schedule.id)}
                        className="ml-auto text-lg hover:scale-110 transition-transform"
                        title="삭제"
                      >
                        🗑️
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-text mb-1">도시</label>
                      <select
                        value={schedule.city}
                        onChange={e => updateCitySchedule(schedule.id, 'city', e.target.value)}
                        required
                        className="w-full px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                        disabled={!country}
                      >
                        <option value="">도시 선택</option>
                        {/* value는 city_name(영문), 화면 표시는 ko_name(한글) */}
                        {cities.map(city => (
                          <option key={city.id} value={city.city_name}>{city.ko_name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-text mb-1">시작일</label>
                      <input
                        type="date"
                        value={schedule.startDate?.split('T')[0]}
                        onChange={e => updateCitySchedule(schedule.id, 'startDate', e.target.value)}
                        min={startDate?.split('T')[0]}
                        max={endDate?.split('T')[0]}
                        required
                        className="w-full px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-text mb-1">종료일</label>
                      <input
                        type="date"
                        value={schedule.endDate?.split('T')[0]}
                        onChange={e => updateCitySchedule(schedule.id, 'endDate', e.target.value)}
                        min={schedule.startDate?.split('T')[0] || startDate?.split('T')[0]}
                        max={endDate?.split('T')[0]}
                        required
                        className="w-full px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                      />
                    </div>
                  </div>

                  {schedule.startDate && schedule.endDate && (
                    <div className="text-xs text-text-soft mt-2">
                      {dayjs(schedule.endDate).diff(dayjs(schedule.startDate), 'day') + 1}일
                    </div>
                  )}
                </div>
              ))}

              <Button
                type="button"
                variant="ghost"
                onClick={addCitySchedule}
                className="self-start"
              >
                + 도시 추가하기
              </Button>
            </>
          )}
        </div>

        <Separator />

        {/* Step 3: 준비물 체크리스트 */}
        <h3 className="text-lg font-semibold text-text">준비물 체크리스트</h3>
        <div>
          <div className="flex flex-col gap-2">
            {checklists.map((item) => (
              <div key={item.id} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={item.is_checked}
                  onChange={(e) => handleUpdateCheck(item.id, 'is_checked', e.target.checked)}
                  className="w-4 h-4 rounded border-primary-dark/20 cursor-pointer"
                />
                <input
                  type="text"
                  value={item.item_name}
                  onChange={(e) => handleUpdateCheck(item.id, 'item_name', e.target.value)}
                  placeholder="준비물 이름"
                  className="flex-1 px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                  disabled={!isEditMode}
                />
                {isEditMode && (
                  <button
                    type="button"
                    onClick={() => handleRemoveCheck(item.id)}
                    className="text-lg hover:scale-110 transition-transform px-2"
                    title="삭제"
                  >
                    🗑️
                  </button>
                )}
              </div>
            ))}
          </div>

          {isEditMode && (
            <Button
              type="button"
              variant="ghost"
              onClick={addCheck}
              className="text-sm"
            >
              + 항목 추가하기
            </Button>
          )}
        </div>

        <Separator />

        {/* Step 3: 일별 스케줄 */}
        {/* 11/2 수정(나영일) : day.date 대신 day.dayNumber를 key로 사용 */}
        <div>
          <h3 className="text-lg font-semibold text-text mb-4">일별 스케줄</h3>
          <div className="flex flex-col gap-3">
            {getDaysList().map((day) => (
              <div key={day.dayNumber} className="border border-primary-dark/20 rounded-lg bg-white overflow-hidden">
                <button
                  type="button"
                  onClick={() => setExpandedDay(expandedDay === day.dayNumber ? null : day.dayNumber)}
                  className="w-full px-4 py-3 flex items-center justify-between hover:bg-primary-dark/5 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="font-semibold text-text">{day.dayNumber}일차</span>
                    <span className="text-sm text-text-soft">{day.date}</span>
                    <span className="text-sm text-primary font-medium">{day.city}</span>
                  </div>
                  <span className="text-text-soft">
                    {expandedDay === day.dayNumber ? '▲' : '▼'}
                  </span>
                </button>

                {expandedDay === day.dayNumber && (
                  <div className="px-4 py-4 border-t border-primary-dark/10 bg-white/50">
                    {/* 시간별 일정 */}
                    <div>
                      <h4 className="text-md font-semibold text-text mb-3">시간별 일정</h4>
                      <div className="flex flex-col gap-3 mb-3">
                        {(dayDetails[day.dayNumber]?.schedules || []).map((schedule) => (
                          <div key={schedule.id} className="p-3 border border-primary-dark/10 rounded-lg bg-white">
                            <div className="flex flex-col gap-2">
                              <input
                                type="text"
                                value={schedule.schedule_content}
                                onChange={(e) => handleUpdateSchedule(day.dayNumber, schedule.id, 'schedule_content', e.target.value)}
                                placeholder="일정 제목"
                                className="px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary font-medium"
                                disabled={!isEditMode}
                              />

                              <div className="grid grid-cols-2 gap-2">
                                <input
                                  type="time"
                                  value={schedule.start_time}
                                  onChange={(e) => handleUpdateSchedule(day.dayNumber, schedule.id, 'start_time', e.target.value)}
                                  placeholder="시작 시간"
                                  className="px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                                  disabled={!isEditMode}
                                />
                                <input
                                  type="time"
                                  value={schedule.end_time}
                                  onChange={(e) => handleUpdateSchedule(day.dayNumber, schedule.id, 'end_time', e.target.value)}
                                  placeholder="종료 시간"
                                  className="px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                                  disabled={!isEditMode}
                                />
                              </div>

                              <input
                                type="text"
                                value={schedule.place}
                                onChange={(e) => handleUpdateSchedule(day.dayNumber, schedule.id, 'place', e.target.value)}
                                placeholder="장소"
                                className="px-3 py-2 rounded-lg border border-primary-dark/20 bg-white text-text text-sm focus:outline-none focus:border-primary"
                                disabled={!isEditMode}
                              />

                              {isEditMode && (
                                <button
                                  type="button"
                                  onClick={() => handleRemoveSchedule(day.dayNumber, schedule.id)}
                                  className="text-lg hover:scale-110 transition-transform self-end"
                                  title="삭제"
                                >
                                  🗑️
                                </button>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                      {isEditMode && (
                        <Button
                          type="button"
                          variant="ghost"
                          onClick={() => addSchedule(day.dayNumber)}
                          className="text-sm"
                        >
                          + 일정 추가하기
                        </Button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  )
}
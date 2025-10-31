import { useState } from 'react'
import api from '../services/api'

export const useTrip = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 여행 생성
  const createTrip = async (tripData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/trips/', tripData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '여행 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 여행 조회
  const getTrip = async (tripId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/${tripId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '여행 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 사용자별 여행 조회
  const getTripsByUser = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/user/${userId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '여행 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 여행 수정
  const updateTrip = async (tripId, tripData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`/trips/${tripId}`, tripData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '여행 수정 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 여행 삭제
  const deleteTrip = async (tripId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/trips/${tripId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '여행 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 일자별 여행 계획 생성
  const createTripDay = async (tripDayData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/trips/days', tripDayData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일자별 계획 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 일자별 여행 계획 조회
  const getTripDays = async (tripId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/days/${tripId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일자별 계획 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 세부 일정 생성
  const createSchedule = async (scheduleData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/trips/schedules', scheduleData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일정 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 세부 일정 조회
  const getSchedule = async (scheduleId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/schedules/${scheduleId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일정 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 일자별 세부 일정 조회
  const getSchedulesByDay = async (tripDayId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/schedules/day/${tripDayId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일정 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 세부 일정 수정
  const updateSchedule = async (scheduleId, scheduleData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`/trips/schedules/${scheduleId}`, scheduleData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일정 수정 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 세부 일정 삭제
  const deleteSchedule = async (scheduleId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/trips/schedules/${scheduleId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '일정 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 체크리스트 항목 생성
  const createChecklistItem = async (itemData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/trips/checklist-items', itemData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '체크리스트 항목 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 체크리스트 항목 조회
  const getChecklistItem = async (itemId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/checklist-items/${itemId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '체크리스트 항목 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 여행별 체크리스트 항목 조회
  const getChecklistItemsByTrip = async (tripId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/checklist-items/trip/${tripId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '체크리스트 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 체크리스트 항목 수정
  const updateChecklistItem = async (itemId, itemData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`/trips/checklist-items/${itemId}`, itemData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '체크리스트 항목 수정 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 체크리스트 항목 삭제
  const deleteChecklistItem = async (itemId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/trips/checklist-items/${itemId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '체크리스트 항목 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // ✅ 알림(날씨용): 백엔드에서 lat/lon 포함된 가장 가까운 여행 조회
  const getNextTrip = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/trips/next/${userId}`)
      return response.data || null
    } catch (err) {
      console.error('❌ 다음 여행 조회 실패:', err)
      setError(err.response?.data?.detail || '다음 여행 조회 실패')
      return null
    } finally {
      setLoading(false)
    }
  }


  return {
    loading,
    error,
    createTrip,
    getTrip,
    getTripsByUser,
    updateTrip,
    deleteTrip,
    createTripDay,
    getTripDays,
    createSchedule,
    getSchedule,
    getSchedulesByDay,
    updateSchedule,
    deleteSchedule,
    createChecklistItem,
    getChecklistItem,
    getChecklistItemsByTrip,
    updateChecklistItem,
    deleteChecklistItem,
    getNextTrip,
  }
}

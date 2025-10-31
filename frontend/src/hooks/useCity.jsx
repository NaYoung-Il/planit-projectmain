import { useState } from 'react'
import api from '../services/api'

export const useCity = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 도시 생성
  const createCity = async (cityData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/cities/', cityData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '도시 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 도시 조회
  const getCity = async (cityId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/cities/${cityId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '도시 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 모든 도시 조회
  const getAllCities = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/cities/')
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '도시 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 도시 이름으로 조회
  const getCityByName = async (cityName) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/cities/name/${cityName}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '도시 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 도시 삭제
  const deleteCity = async (cityId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/cities/${cityId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '도시 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 장소 생성
  const createPlace = async (placeData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/cities/places', placeData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '장소 생성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 장소 조회
  const getPlace = async (placeId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/cities/places/${placeId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '장소 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 모든 장소 조회
  const getAllPlaces = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/cities/places')
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '장소 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 특정 도시의 모든 장소 조회
  const getPlacesByCity = async (cityId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/cities/places/city/${cityId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '장소 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 장소 삭제
  const deletePlace = async (placeId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/cities/places/${placeId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '장소 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    createCity,
    getCity,
    getAllCities,
    getCityByName,
    deleteCity,
    createPlace,
    getPlace,
    getAllPlaces,
    getPlacesByCity,
    deletePlace,
  }
}

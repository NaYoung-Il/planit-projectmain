import { useState } from 'react'
import api from '../services/api'

export const useReview = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 리뷰 작성
  const createReview = async (reviewData, tripId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post(`/reviews/?trip_id=${tripId}`, reviewData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '리뷰 작성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 리뷰 목록 조회
  const getReviews = async (tripId, params = {}) => {
    setLoading(true)
    setError(null)
    try {
      const { search, limit = 10, offset = 0 } = params
      const queryParams = new URLSearchParams({ trip_id: tripId, limit, offset })
      if (search) queryParams.append('search', search)

      const response = await api.get(`/reviews/?${queryParams}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '리뷰 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 리뷰 상세 조회
  const getReview = async (reviewId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/reviews/${reviewId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '리뷰 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 리뷰 수정
  const updateReview = async (reviewId, reviewData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`/reviews/${reviewId}`, reviewData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '리뷰 수정 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 리뷰 삭제
  const deleteReview = async (reviewId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/reviews/${reviewId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '리뷰 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    createReview,
    getReviews,
    getReview,
    updateReview,
    deleteReview,
  }
}

import { useState } from 'react'
import api from '../services/api'

export const useLike = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 좋아요 토글 (추가/취소)
  const toggleLike = async (reviewId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post(`/reviews/${reviewId}/likes`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '좋아요 처리 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 좋아요 수 조회
  const getLikes = async (reviewId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/reviews/${reviewId}/likes`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '좋아요 수 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    toggleLike,
    getLikes,
  }
}

import { useState } from 'react'
import api from '../services/api'

export const useComment = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 댓글 작성
  const createComment = async (reviewId, commentData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post(`/reviews/${reviewId}/comments/`, commentData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '댓글 작성 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 댓글 목록 조회
  const getComments = async (reviewId, params = {}) => {
    setLoading(true)
    setError(null)
    try {
      const { search, limit = 10, offset = 0 } = params
      const queryParams = new URLSearchParams({ limit, offset })
      if (search) queryParams.append('search', search)

      const response = await api.get(`/reviews/${reviewId}/comments/?${queryParams}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '댓글 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 댓글 상세 조회
  const getComment = async (reviewId, commentId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/reviews/${reviewId}/comments/${commentId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '댓글 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 댓글 수정
  const updateComment = async (reviewId, commentId, commentData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`/reviews/${reviewId}/comments/${commentId}`, commentData)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '댓글 수정 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 댓글 삭제
  const deleteComment = async (reviewId, commentId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/reviews/${reviewId}/comments/delete/${commentId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '댓글 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    createComment,
    getComments,
    getComment,
    updateComment,
    deleteComment,
  }
}

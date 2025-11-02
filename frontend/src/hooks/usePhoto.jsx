import { useState } from 'react'
import api from '../services/api'

export const usePhoto = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 사진 업로드
  const uploadPhoto = async (reviewId, file) => {
    setLoading(true)
    setError(null)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await api.post(`/reviews/${reviewId}/photos/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '사진 업로드 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 사진 목록 조회
  const getPhotos = async (reviewId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/reviews/${reviewId}/photos/`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '사진 목록 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 사진 상세 조회
  const getPhoto = async (reviewId, photoId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(`/reviews/${reviewId}/photos/${photoId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '사진 조회 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 사진 원본 URL 가져오기
  const getPhotoRawUrl = (reviewId, photoId) => {
    return `${api.defaults.baseURL}/reviews/${reviewId}/photos/${photoId}/raw`
  }

  // 사진 삭제
  const deletePhoto = async (reviewId, photoId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.delete(`/reviews/${reviewId}/photos/${photoId}`)
      return response.data
    } catch (err) {
      setError(err.response?.data?.detail || '사진 삭제 실패')
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    uploadPhoto,
    getPhotos,
    getPhoto,
    getPhotoRawUrl,
    deletePhoto,
  }
}

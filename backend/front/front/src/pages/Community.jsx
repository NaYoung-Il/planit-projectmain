import { useEffect, useRef, useState } from 'react'
import Card from '../components/Card'
import { useReview } from '../hooks/useReview'
import { useComment } from '../hooks/useComment'
import { useLike } from '../hooks/useLike'
import { usePhoto } from '../hooks/usePhoto'
import { useAuth } from '../hooks/useAuth'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

// 페이지: 리뷰/댓글/좋아요 기능이 있는 커뮤니티
export default function Community(){
  const [text, setText] = useState('')
  const [photo, setPhoto] = useState(null)
  const [reviews, setReviews] = useState([])
  const [fileName, setFileName] = useState('')
  const [tripId, setTripId] = useState(1) // 임시 여행 ID
  const fileRef = useRef()

  const { getCurrentUser } = useAuth()
  const { createReview, getReviews, deleteReview } = useReview()
  const { uploadPhoto } = usePhoto()
  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)

        // 리뷰 목록 조회
        const reviewList = await getReviews(tripId)
        setReviews(reviewList)
      } catch (err) {
        console.error('데이터 조회 실패:', err)
      }
    }
    fetchData()
  }, [])

  const refresh = async () => {
    try {
      const reviewList = await getReviews(tripId)
      setReviews(reviewList)
    } catch (err) {
      console.error('리뷰 목록 조회 실패:', err)
    }
  }

  const onUpload = async (file) => {
    if(!file) return
    setPhoto(file)
    setFileName(file.name)
  }

  const submit = async (e) => {
    e.preventDefault()
    if(!text && !photo) return

    try {
      // 리뷰 작성
      const newReview = await createReview({ content: text }, tripId)

      // 사진이 있으면 업로드
      if(photo) {
        await uploadPhoto(newReview.id, photo)
      }

      setText('')
      setPhoto(null)
      setFileName('')
      if(fileRef.current) fileRef.current.value = ''

      await refresh()
    } catch (err) {
      alert('후기 작성에 실패했습니다')
    }
  }

  const del = async (id) => {
    try {
      await deleteReview(id)
      await refresh()
    } catch (err) {
      alert('삭제에 실패했습니다')
    }
  }

  return (
    <div className="grid gap-6 relative z-[1] mt-6 grid-cols-1">
      <div className="col-span-full">
        <Card title="새 후기" subtitle="사진은 선택입니다.">
          <form className="flex flex-col gap-3" onSubmit={submit}>
            <textarea
              className="w-full min-h-[160px] rounded-lg p-4 bg-white/55 backdrop-blur border border-primary-dark/12 text-text text-sm leading-relaxed resize-y outline-none transition shadow-sm focus:border-primary focus:shadow-[0_0_0_3px_rgba(16,185,129,0.18)] focus:bg-white/70 placeholder:text-text-soft/70"
              value={text}
              onChange={e=>setText(e.target.value)}
              placeholder="여행 후기를 적어주세요..."
            />
            <div className="flex items-center gap-2.5 w-full max-w-[520px]">
              <button type="button" className="px-3.5 py-2.5 rounded-xl bg-gradient-primary text-white border-0 shadow-sm text-sm" onClick={()=>fileRef.current?.click()}>파일 선택</button>
              <div className="flex-1 min-h-[40px] flex items-center px-3.5 border border-primary-dark/16 rounded-xl bg-white text-text text-sm min-w-[220px]">{fileName || '선택된 파일 없음'}</div>
            </div>
            <input ref={fileRef} type="file" accept="image/*" onChange={e=>onUpload(e.target.files?.[0])} className="hidden" />
            {photo && <img className="mt-2 max-h-[220px] rounded-xl shadow" src={URL.createObjectURL(photo)} alt="preview" />}
            <Button variant="primary" type="submit">올리기</Button>
          </form>
        </Card>
      </div>

      <div className="col-span-full flex flex-col gap-6">
        {reviews.map(review=> (
          <ReviewCard
            key={review.id}
            review={review}
            onDelete={del}
            onRefresh={refresh}
            currentUser={user}
          />
        ))}
      </div>
    </div>
  )
}

// 리뷰 카드 컴포넌트
function ReviewCard({review, onDelete, onRefresh, currentUser}) {
  const { toggleLike, getLikes } = useLike()
  const { getComments, createComment, deleteComment } = useComment()
  const { getPhotos } = usePhoto()

  const [likes, setLikes] = useState({ count: 0, is_liked: false })
  const [comments, setComments] = useState([])
  const [photos, setPhotos] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [likeData, commentList, photoList] = await Promise.all([
          getLikes(review.id),
          getComments(review.id),
          getPhotos(review.id)
        ])
        setLikes(likeData)
        setComments(commentList)
        setPhotos(photoList)
      } catch (err) {
        console.error('리뷰 상세 정보 조회 실패:', err)
      }
    }
    fetchData()
  }, [review.id])

  const handleLike = async () => {
    try {
      const result = await toggleLike(review.id)
      setLikes(result)
    } catch (err) {
      console.error('좋아요 처리 실패:', err)
    }
  }

  const handleAddComment = async (text) => {
    if(!text) return
    try {
      await createComment(review.id, { content: text })
      const commentList = await getComments(review.id)
      setComments(commentList)
    } catch (err) {
      alert('댓글 작성에 실패했습니다')
    }
  }

  const handleDeleteComment = async (commentId) => {
    try {
      await deleteComment(review.id, commentId)
      const commentList = await getComments(review.id)
      setComments(commentList)
    } catch (err) {
      alert('댓글 삭제에 실패했습니다')
    }
  }

  return (
    <Card
      key={review.id}
      title={review.user?.username || review.user?.email || '작성자'}
      right={currentUser?.id === review.user_id && <Button variant="ghost" size="sm" onClick={()=>onDelete(review.id)}>삭제</Button>}
    >
      <div className="flex flex-col gap-2.5">
        {photos.length > 0 && (
          <img
            className="w-full max-h-[360px] object-cover rounded-xl"
            src={photos[0].url || photos[0].data}
            alt="review"
          />
        )}
        {review.content && <p className="my-2.5">{review.content}</p>}
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={handleLike}>
            {likes.is_liked ? '❤️' : '🤍'} {likes.count}
          </Button>
        </div>
        <div className="flex flex-col gap-2 mt-2.5">
          {comments.map(c=> (
            <div key={c.id} className="bg-surface border border-primary-dark/16 px-2.5 py-2 rounded-lg text-sm flex justify-between items-center">
              <div><b>{c.user?.username || c.user?.email}:</b> {c.content}</div>
              {currentUser?.id === c.user_id && (
                <Button variant="ghost" size="sm" onClick={()=>handleDeleteComment(c.id)}>삭제</Button>
              )}
            </div>
          ))}
          <CommentInput onSubmit={handleAddComment} />
        </div>
      </div>
    </Card>
  )
}

// 댓글 입력 컴포넌트
function CommentInput({onSubmit}){
  const [v, setV] = useState('')
  return (
    <div className="flex gap-2">
      <Input
        className="flex-1"
        placeholder="댓글 달기"
        value={v}
        onChange={e=>setV(e.target.value)}
      />
      <Button variant="ghost" size="sm" onClick={()=>{ onSubmit(v); setV('') }}>게시</Button>
    </div>
  )
}

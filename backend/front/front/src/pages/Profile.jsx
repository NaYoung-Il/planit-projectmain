import Card from '../components/Card'
import { useAuth } from '../hooks/useAuth'
import { useState, useRef, useEffect } from 'react'
import FormField from '../components/ui/FormField'
import Button from '../components/ui/Button'

// Profile : 닉네임/아바타 편집
export default function Profile(){
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [avatar, setAvatar] = useState('')
  const [avatarFileName, setAvatarFileName] = useState('')
  const fileRef = useRef()
  const { getCurrentUser, updateUser, loading, error } = useAuth()

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser()
        setName(user.username || '')
        setEmail(user.email || '')
      } catch (err) {
        console.error('사용자 정보 조회 실패:', err)
      }
    }
    fetchUser()
  }, [])

  const save = async ()=>{
    try {
      await updateUser({ username: name })
      alert('저장되었습니다')
    } catch (err) {
      alert('저장에 실패했습니다: ' + (error || '알 수 없는 오류'))
    }
  }
  const onUpload = (f)=>{
    if(!f) return
    const reader = new FileReader();
    reader.onload=()=> setAvatar(reader.result);
    reader.readAsDataURL(f)
    setAvatarFileName(f.name)
  }
  return (
    <Card title="프로필 편집" className="overflow-visible">
      <form className="flex flex-col gap-4 max-w-[420px]" onSubmit={e=>{e.preventDefault();save()}}>
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-8">
          <div className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl font-semibold overflow-hidden flex-shrink-0 shadow-button border-2 ${avatar ? 'bg-gradient-primary p-0.5' : 'bg-gradient-primary text-white'}`}>
            {avatar ? <img src={avatar} alt="아바타" className="w-full h-full object-cover rounded-full" /> : (name?.[0]?.toUpperCase()||'U')}
          </div>
          <div className="flex flex-col gap-5 w-full">
            <FormField
              label="닉네임"
              value={name}
              onChange={e=>setName(e.target.value)}
              className="w-full"
            />
            <div className="flex flex-col gap-2 text-xs font-semibold text-text-soft">
              <span>아바타 이미지</span>
              <div className="flex items-center gap-3 w-full">
                <button type="button" className="px-4 py-2 rounded-lg bg-gradient-primary text-white text-xs font-semibold shadow-button hover:-translate-y-px transition" onClick={()=>fileRef.current?.click()}>업로드</button>
                <div className="flex-1 min-h-[40px] px-3 py-2 rounded-lg border border-primary-dark/20 bg-surface text-text text-xs flex items-center">{avatarFileName || '선택된 파일 없음'}</div>
              </div>
              <input ref={fileRef} type="file" accept="image/*" onChange={e=>onUpload(e.target.files?.[0])} className="hidden" />
            </div>
          </div>
        </div>
        <Button variant="primary" type="submit" className="mt-4">저장</Button>
      </form>
    </Card>
  )
}

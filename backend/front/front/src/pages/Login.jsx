import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import FormField from '../components/ui/FormField'
import Button from '../components/ui/Button'

// Login: Backend API를 이용한 로그인
export default function Login(){
  const [email,setEmail] = useState('')
  const [pw,setPw] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const nav = useNavigate()
  const loc = useLocation()
  const { login, loading, error } = useAuth()

  const submit = async (e)=>{
    e.preventDefault()
    setErrorMsg('')
    try {
      await login(email, pw)
      const back = loc.state?.from || '/'
      nav(back, { replace: true })
    } catch (err) {
      setErrorMsg(error || '로그인에 실패했습니다.')
    }
  }
  return (
    <div className="min-h-dvh grid place-items-center p-12 px-4">
      <form className="w-[380px] max-w-full bg-surface border border-primary-dark/18 shadow-[0_10px_28px_rgba(16,185,129,0.08)] rounded-lg backdrop-blur" onSubmit={submit}>
        <div className="p-5 pt-5 pb-0">
          <h3 className="m-0 text-base font-bold text-text">로그인</h3>
        </div>
        <div className="p-5 pt-4 pb-6 flex flex-col gap-3.5">
          <FormField
            label="이메일"
            type="email"
            value={email}
            onChange={e=>setEmail(e.target.value)}
            required
          />
          <FormField
            label="비밀번호"
            type="password"
            value={pw}
            onChange={e=>setPw(e.target.value)}
            required
          />
          {errorMsg && <div className="text-red-500 text-xs">{errorMsg}</div>}
          <Button variant="primary" type="submit" disabled={loading} className="w-full h-11 !text-sm !font-semibold tracking-wide">
            {loading ? '로그인 중...' : '로그인'}
          </Button>
        </div>
      </form>
    </div>
  )
}

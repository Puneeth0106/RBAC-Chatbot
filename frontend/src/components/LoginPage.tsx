import { useState, FormEvent } from 'react'
import { Auth, Role } from '../types'
import { Eye, EyeOff, ChevronDown, Shield } from 'lucide-react'

interface Props {
  onLogin: (auth: Auth) => void
}

const DEMO_USERS: { username: string; password: string; role: Role }[] = [
  { username: 'Tony', password: 'password123', role: 'engineering' },
  { username: 'Peter', password: 'pete123', role: 'engineering' },
  { username: 'Bruce', password: 'securepass', role: 'marketing' },
  { username: 'Sid', password: 'sidpass123', role: 'marketing' },
  { username: 'Sam', password: 'financepass', role: 'finance' },
  { username: 'Natasha', password: 'hrpass123', role: 'hr' },
]

const ROLE_PILL: Record<Role, string> = {
  engineering: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  marketing:   'text-amber-400 bg-amber-500/10 border-amber-500/20',
  finance:     'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  hr:          'text-violet-400 bg-violet-500/10 border-violet-500/20',
}

const API_BASE = import.meta.env.VITE_API_URL ?? ''

export default function LoginPage({ onLogin }: Props) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showDemo, setShowDemo] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const credentials = btoa(`${username}:${password}`)
      const res = await fetch(`${API_BASE}/login`, {
        headers: { Authorization: `Basic ${credentials}` },
      })
      if (!res.ok) throw new Error('Invalid credentials')
      const data = await res.json()
      onLogin({ username, role: data.role as Role, credentials })
    } catch {
      setError('Invalid username or password. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  function fillDemo(user: typeof DEMO_USERS[0]) {
    setUsername(user.username)
    setPassword(user.password)
    setError('')
    setShowDemo(false)
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{
        background:
          'radial-gradient(ellipse 80% 60% at 70% 0%, rgba(99,102,241,0.13) 0%, transparent 60%),' +
          'radial-gradient(ellipse 60% 50% at 10% 100%, rgba(139,92,246,0.09) 0%, transparent 55%),' +
          '#0d0d14',
      }}
    >
      <div className="w-full max-w-[400px]">

        {/* Wordmark */}
        <div className="flex flex-col items-center mb-8">
          <div className="flex items-center gap-2.5 mb-2">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-600/30">
              <span className="text-white font-bold text-xl tracking-tight">F</span>
            </div>
            <span className="text-2xl font-bold text-white tracking-tight">FinSolve</span>
          </div>
          <p className="text-slate-500 text-sm">Internal Intelligence Platform</p>
        </div>

        {/* Card */}
        <div
          className="rounded-2xl border border-white/8 p-8"
          style={{ background: 'rgba(16,16,26,0.85)', backdropFilter: 'blur(16px)' }}
        >
          <div className="flex items-center gap-2 mb-1">
            <Shield size={14} className="text-indigo-400" />
            <h1 className="text-base font-semibold text-white">Secure sign‑in</h1>
          </div>
          <p className="text-slate-500 text-xs mb-6 pl-5">
            Access is scoped to your assigned role
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username */}
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
                autoComplete="username"
                className="w-full px-3.5 py-2.5 rounded-xl text-sm text-white placeholder-slate-600 bg-white/5 border border-white/10 outline-none focus:border-indigo-500/60 focus:ring-2 focus:ring-indigo-500/15 transition-all duration-150"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                  className="w-full px-3.5 py-2.5 pr-11 rounded-xl text-sm text-white placeholder-slate-600 bg-white/5 border border-white/10 outline-none focus:border-indigo-500/60 focus:ring-2 focus:ring-indigo-500/15 transition-all duration-150"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(v => !v)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="flex items-start gap-2 px-3.5 py-2.5 rounded-xl bg-red-500/8 border border-red-500/20">
                <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-1 shrink-0" />
                <p className="text-red-400 text-xs leading-relaxed">{error}</p>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium transition-all duration-150 flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/25 border-t-white rounded-full animate-spin" />
                  Signing in…
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>
        </div>

        {/* Demo credentials */}
        <div
          className="mt-3 rounded-2xl border border-white/6 overflow-hidden"
          style={{ background: 'rgba(16,16,26,0.6)' }}
        >
          <button
            onClick={() => setShowDemo(v => !v)}
            className="w-full flex items-center justify-between px-5 py-3.5 text-xs text-slate-500 hover:text-slate-300 transition-colors"
          >
            <span className="font-medium">Demo accounts</span>
            <ChevronDown
              size={13}
              className={`transition-transform duration-200 ${showDemo ? 'rotate-180' : ''}`}
            />
          </button>

          {showDemo && (
            <div className="border-t border-white/6">
              {DEMO_USERS.map(user => (
                <button
                  key={user.username}
                  onClick={() => fillDemo(user)}
                  className="w-full flex items-center justify-between px-5 py-2.5 hover:bg-white/4 transition-colors text-left group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-7 h-7 rounded-full bg-indigo-600/20 border border-indigo-500/20 flex items-center justify-center shrink-0">
                      <span className="text-indigo-300 text-xs font-semibold">
                        {user.username[0]}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm text-slate-300 group-hover:text-white transition-colors">
                        {user.username}
                      </p>
                      <p className="text-xs text-slate-600">{user.password}</p>
                    </div>
                  </div>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full border ${ROLE_PILL[user.role]}`}
                  >
                    {user.role}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        <p className="text-center text-xs text-slate-700 mt-5">
          FinSolve · Restricted internal access
        </p>
      </div>
    </div>
  )
}

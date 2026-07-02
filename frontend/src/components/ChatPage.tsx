import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  Send, LogOut, Plus, Bot, FileText,
  ChevronDown, ChevronUp, Zap, Sparkles,
} from 'lucide-react'
import { Auth, Message, Source, Role } from '../types'

// ─── Role config ────────────────────────────────────────────────────────────

const ROLE: Record<Role, {
  label: string
  bg: string; text: string; border: string; dot: string; ring: string
}> = {
  engineering: {
    label: 'Engineering',
    bg: 'bg-blue-500/12', text: 'text-blue-400',
    border: 'border-blue-500/25', dot: 'bg-blue-400', ring: 'ring-blue-500/20',
  },
  marketing: {
    label: 'Marketing',
    bg: 'bg-amber-500/12', text: 'text-amber-400',
    border: 'border-amber-500/25', dot: 'bg-amber-400', ring: 'ring-amber-500/20',
  },
  finance: {
    label: 'Finance',
    bg: 'bg-emerald-500/12', text: 'text-emerald-400',
    border: 'border-emerald-500/25', dot: 'bg-emerald-400', ring: 'ring-emerald-500/20',
  },
  hr: {
    label: 'Human Resources',
    bg: 'bg-violet-500/12', text: 'text-violet-400',
    border: 'border-violet-500/25', dot: 'bg-violet-400', ring: 'ring-violet-500/20',
  },
}

const WELCOME_PROMPTS: Record<Role, string[]> = {
  engineering: [
    'What is our current tech stack?',
    'How do I set up the local dev environment?',
    'Walk me through our API design guidelines.',
  ],
  marketing: [
    'Summarise our brand guidelines.',
    'What are our target customer segments?',
    'What campaigns are currently running?',
  ],
  finance: [
    'Give me a Q4 financial summary.',
    'What are our expense reporting policies?',
    'How is the current budget allocated?',
  ],
  hr: [
    'What is our leave and PTO policy?',
    'How does the performance review process work?',
    'What benefits does FinSolve offer?',
  ],
}

// ─── Helpers ────────────────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_URL ?? ''

function uid() {
  return Math.random().toString(36).slice(2, 11)
}

function shortName(path: string) {
  const file = path.split('/').pop() ?? path
  return file.replace(/\.(md|txt|pdf)$/i, '').replace(/[-_]/g, ' ')
}

// ─── Sources panel ──────────────────────────────────────────────────────────

function SourcesPanel({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState(true)
  if (!sources.length) return null

  return (
    <div className="mt-3 rounded-xl border border-white/8 overflow-hidden text-xs"
      style={{ background: 'rgba(255,255,255,0.02)' }}>
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center gap-2 px-3 py-2 hover:bg-white/3 transition-colors"
      >
        <FileText size={11} className="text-slate-600 shrink-0" />
        <span className="flex-1 text-left text-slate-500">
          {sources.length} source{sources.length !== 1 ? 's' : ''}
        </span>
        {open
          ? <ChevronUp size={11} className="text-slate-600" />
          : <ChevronDown size={11} className="text-slate-600" />}
      </button>

      {open && (
        <div className="border-t border-white/6 px-3 py-2.5 flex flex-wrap gap-1.5">
          {sources.map((src, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/4 border border-white/8 text-slate-400 capitalize"
            >
              <FileText size={9} className="text-slate-600 shrink-0" />
              {shortName(src.source)}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Suggestions panel ──────────────────────────────────────────────────────

function SuggestionsPanel({
  suggestions,
  onSelect,
}: {
  suggestions: string[]
  onSelect: (q: string) => void
}) {
  if (!suggestions.length) return null
  return (
    <div className="mt-3">
      <p className="text-xs text-slate-600 mb-2">Follow-up questions</p>
      <div className="flex flex-col gap-1.5">
        {suggestions.map((q, i) => (
          <button
            key={i}
            onClick={() => onSelect(q)}
            className="text-left text-xs px-3 py-2 rounded-lg border border-white/8 hover:border-indigo-500/30 bg-white/2 hover:bg-indigo-500/8 text-slate-400 hover:text-slate-200 transition-all"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}

// ─── Message bubble ─────────────────────────────────────────────────────────

function MessageBubble({
  message,
  rc,
  onSuggestionClick,
}: {
  message: Message
  rc: typeof ROLE[Role]
  onSuggestionClick: (q: string) => void
}) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[76%] px-4 py-3 rounded-2xl rounded-tr-sm text-sm leading-relaxed text-slate-100"
          style={{ background: 'rgba(99,102,241,0.18)', border: '1px solid rgba(99,102,241,0.22)' }}>
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${rc.bg} border ${rc.border}`}>
        <Bot size={13} className={rc.text} />
      </div>

      <div className="flex-1 min-w-0">
        {/* Content */}
        <div className="text-sm leading-relaxed text-slate-200">
          {message.content ? (
            <>
              <div className="prose prose-sm prose-invert max-w-none
                prose-p:my-1.5 prose-ul:my-1.5 prose-ol:my-1.5
                prose-li:my-0.5 prose-headings:font-semibold
                prose-headings:text-slate-100 prose-headings:mt-3 prose-headings:mb-1
                prose-code:text-indigo-300 prose-code:bg-white/8 prose-code:px-1
                prose-code:py-0.5 prose-code:rounded prose-code:text-xs
                prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
                prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-xl
                prose-strong:text-slate-100 prose-a:text-indigo-400">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </div>
              {message.isStreaming && (
                <span className="inline-block w-0.5 h-4 bg-indigo-400 ml-0.5 cursor-blink align-text-bottom" />
              )}
            </>
          ) : message.isStreaming ? (
            <div className="flex items-center gap-1 py-1">
              {[0, 150, 300].map(delay => (
                <div
                  key={delay}
                  className="w-1.5 h-1.5 rounded-full bg-slate-600 animate-bounce"
                  style={{ animationDelay: `${delay}ms` }}
                />
              ))}
            </div>
          ) : null}
        </div>

        {!message.isStreaming && message.sources && (
          <SourcesPanel sources={message.sources} />
        )}
        {!message.isStreaming && message.suggestions && (
          <SuggestionsPanel suggestions={message.suggestions} onSelect={onSuggestionClick} />
        )}
      </div>
    </div>
  )
}

// ─── Chat page ───────────────────────────────────────────────────────────────

interface Props {
  auth: Auth
  onLogout: () => void
}

export default function ChatPage({ auth, onLogout }: Props) {
  const role = auth.role
  const rc = ROLE[role]

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(uid)
  const loadingRef = useRef(false)
  const [isLoading, setIsLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function resetTextarea() {
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }

  function handleNewChat() {
    setMessages([])
    setSessionId(uid())
    setInput('')
    resetTextarea()
  }

  async function sendMessage(text: string) {
    const trimmed = text.trim()
    if (!trimmed || loadingRef.current) return

    loadingRef.current = true
    setIsLoading(true)

    const userMsg: Message = {
      id: uid(), role: 'user', content: trimmed, timestamp: new Date(),
    }
    const asstId = uid()
    const asstMsg: Message = {
      id: asstId, role: 'assistant', content: '', isStreaming: true, timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMsg, asstMsg])
    setInput('')
    resetTextarea()

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Basic ${auth.credentials}`,
        },
        body: JSON.stringify({ message: trimmed, session_id: sessionId }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Request failed' }))
        throw new Error(err.detail ?? 'Request failed')
      }

      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buf = ''
      let sources: Source[] = []
      let fullAnswer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const lines = buf.split('\n')
        buf = lines.pop() ?? ''

        for (const line of lines) {
          if (!line.trim()) continue
          const frame = JSON.parse(line)
          if (frame.type === 'sources') {
            sources = frame.sources ?? []
          } else if (frame.type === 'token') {
            fullAnswer += frame.content
            setMessages(prev =>
              prev.map(m =>
                m.id === asstId ? { ...m, content: m.content + frame.content } : m,
              ),
            )
          } else if (frame.type === 'done') {
            setMessages(prev =>
              prev.map(m =>
                m.id === asstId ? { ...m, isStreaming: false, sources } : m,
              ),
            )
          }
        }
      }

      // Fetch follow-up suggestions in the background after stream ends
      if (fullAnswer) {
        fetch(`${API_BASE}/suggestions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Basic ${auth.credentials}`,
          },
          body: JSON.stringify({ question: trimmed, answer: fullAnswer }),
        })
          .then(r => r.json())
          .then(data => {
            setMessages(prev =>
              prev.map(m =>
                m.id === asstId ? { ...m, suggestions: data.suggestions } : m,
              ),
            )
          })
          .catch(() => {})
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Something went wrong.'
      setMessages(prev =>
        prev.map(m =>
          m.id === asstId ? { ...m, content: `⚠ ${msg}`, isStreaming: false } : m,
        ),
      )
    } finally {
      loadingRef.current = false
      setIsLoading(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  return (
    <div className="h-screen flex overflow-hidden" style={{ background: '#0d0d14' }}>

      {/* ── Sidebar ────────────────────────────────────── */}
      <aside
        className="w-56 shrink-0 flex flex-col border-r border-white/6"
        style={{ background: 'rgba(11,11,18,0.97)' }}
      >
        {/* Logo */}
        <div className="px-4 py-4 border-b border-white/6">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center shadow-md shadow-indigo-600/30">
              <span className="text-white font-bold text-sm">F</span>
            </div>
            <span className="font-semibold text-white text-sm tracking-tight">FinSolve</span>
          </div>
        </div>

        {/* New chat */}
        <div className="px-3 py-3">
          <button
            onClick={handleNewChat}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-slate-400 hover:text-white border border-white/8 hover:border-white/15 hover:bg-white/4 transition-all"
          >
            <Plus size={13} />
            New conversation
          </button>
        </div>

        <div className="flex-1" />

        {/* User card */}
        <div className="px-3 pb-4 border-t border-white/6 pt-3">
          <div className="rounded-xl p-3 border border-white/8" style={{ background: 'rgba(255,255,255,0.025)' }}>
            {/* Avatar + name */}
            <div className="flex items-center gap-2.5 mb-2.5">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ring-2 ${rc.ring} ${rc.bg} ${rc.text}`}>
                {auth.username[0]}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-white truncate leading-none mb-0.5">
                  {auth.username}
                </p>
                <p className="text-xs text-slate-600 leading-none">FinSolve</p>
              </div>
            </div>

            {/* Role badge */}
            <div className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border mb-2.5 ${rc.bg} ${rc.border}`}>
              <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${rc.dot}`} />
              <span className={`text-xs font-medium ${rc.text}`}>{rc.label}</span>
            </div>

            {/* Logout */}
            <button
              onClick={onLogout}
              className="w-full flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs text-slate-600 hover:text-slate-300 hover:bg-white/5 transition-all"
            >
              <LogOut size={11} />
              Sign out
            </button>
          </div>
        </div>
      </aside>

      {/* ── Main ───────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0">

        {/* Header */}
        <header className="px-6 py-3 border-b border-white/6 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2.5">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${rc.bg} border ${rc.border}`}>
              <Zap size={14} className={rc.text} />
            </div>
            <div>
              <p className="text-sm font-semibold text-white leading-none mb-0.5">FinSolve AI</p>
              <p className="text-xs text-slate-600 leading-none">Role-scoped intelligence</p>
            </div>
          </div>
          <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full border text-xs font-medium ${rc.bg} ${rc.text} ${rc.border}`}>
            <div className={`w-1.5 h-1.5 rounded-full ${rc.dot}`} />
            {rc.label} access
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center select-none">
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-5 ${rc.bg} border ${rc.border}`}>
                <Sparkles size={26} className={rc.text} />
              </div>
              <h2 className="text-xl font-semibold text-white mb-1">
                Hello, {auth.username}
              </h2>
              <p className="text-sm text-slate-500 mb-8 max-w-xs leading-relaxed">
                I can answer questions using documents scoped to your{' '}
                <span className={rc.text}>{role}</span> clearance level.
              </p>
              <div className="grid gap-2 w-full max-w-sm">
                {WELCOME_PROMPTS[role].map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(prompt)}
                    disabled={isLoading}
                    className="text-left px-4 py-3 rounded-xl border border-white/8 hover:border-white/15 bg-white/2 hover:bg-white/4 text-sm text-slate-400 hover:text-slate-200 transition-all disabled:opacity-40"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map(msg => (
              <MessageBubble key={msg.id} message={msg} rc={rc} onSuggestionClick={sendMessage} />
            ))
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="px-6 pb-5 pt-3 shrink-0 border-t border-white/6">
          <div
            className="flex gap-3 items-end rounded-2xl border border-white/10 focus-within:border-indigo-500/40 focus-within:ring-2 focus-within:ring-indigo-500/12 transition-all p-3.5"
            style={{ background: 'rgba(255,255,255,0.035)' }}
          >
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => {
                setInput(e.target.value)
                const el = e.target
                el.style.height = 'auto'
                el.style.height = Math.min(el.scrollHeight, 160) + 'px'
              }}
              onKeyDown={handleKeyDown}
              placeholder={`Ask about ${rc.label.toLowerCase()} data…`}
              rows={1}
              disabled={isLoading}
              className="flex-1 resize-none bg-transparent text-sm text-white placeholder-slate-600 outline-none leading-relaxed disabled:opacity-50"
              style={{ minHeight: '22px', maxHeight: '160px' }}
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || isLoading}
              className={`w-8 h-8 flex items-center justify-center rounded-xl shrink-0 transition-all duration-150
                ${input.trim() && !isLoading
                  ? 'bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-600/30'
                  : 'bg-white/8 opacity-40 cursor-not-allowed'}`}
            >
              {isLoading
                ? <div className="w-3.5 h-3.5 border-2 border-white/25 border-t-white rounded-full animate-spin" />
                : <Send size={13} className="text-white" />}
            </button>
          </div>
          <p className="text-center text-xs text-slate-700 mt-2">
            Responses are limited to your {role} clearance · Enter to send · Shift+Enter for newline
          </p>
        </div>

      </div>
    </div>
  )
}

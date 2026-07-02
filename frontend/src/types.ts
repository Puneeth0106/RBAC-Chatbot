export type Role = 'engineering' | 'marketing' | 'finance' | 'hr'

export interface Auth {
  username: string
  role: Role
  credentials: string // base64 Basic auth token
}

export interface Source {
  source: string
  role: string
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
  isStreaming?: boolean
  timestamp: Date
}

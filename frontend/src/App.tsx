import { useState } from 'react'
import { Auth } from './types'
import LoginPage from './components/LoginPage'
import ChatPage from './components/ChatPage'

export default function App() {
  const [auth, setAuth] = useState<Auth | null>(null)

  return auth
    ? <ChatPage auth={auth} onLogout={() => setAuth(null)} />
    : <LoginPage onLogin={setAuth} />
}

import React, { useEffect, useState } from 'react'
import App from './App'
import { API_ROOT } from './utils/apiBase'
import { setCsrfToken, sessionHeaders } from './utils/session'

export default function AuthGate() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  function acceptSession(data) {
    setCsrfToken(data.csrf_token)
    setUser(data.user)
    setPassword('')
  }

  useEffect(() => {
    let active = true
    fetch(`${API_ROOT}/auth/session`, { credentials: 'include' })
      .then(async response => {
        if (response.status === 401) return
        if (!response.ok) throw new Error()
        const data = await response.json()
        if (active) acceptSession(data)
      })
      .catch(() => { if (active) setError('Die Anmeldung konnte nicht geprüft werden. Bitte erneut versuchen.') })
      .finally(() => { if (active) setLoading(false) })
    const expired = () => {
      setCsrfToken('')
      setUser(null)
      setError('Deine Sitzung ist abgelaufen. Bitte erneut anmelden.')
    }
    window.addEventListener('paperless-session-expired', expired)
    return () => { active = false; window.removeEventListener('paperless-session-expired', expired) }
  }, [])

  async function login(event) {
    event.preventDefault()
    if (pending) return
    setPending(true)
    setError('')
    try {
      const response = await fetch(`${API_ROOT}/auth/login`, {
        method: 'POST', credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'X-Paperless-Login': '1' },
        body: JSON.stringify({ username, password })
      })
      if (!response.ok) {
        setError(response.status === 429 ? 'Zu viele Anmeldeversuche. Bitte später erneut versuchen.' : 'Anmeldung fehlgeschlagen. Prüfe Benutzername und Passwort.')
        return
      }
      acceptSession(await response.json())
    } catch { setError('Der Server ist nicht erreichbar. Bitte erneut versuchen.') }
    finally { setPassword(''); setPending(false) }
  }

  async function logout() {
    setPending(true)
    setError('')
    try {
      const response = await fetch(`${API_ROOT}/auth/logout`, {
        method: 'POST', credentials: 'include', headers: sessionHeaders()
      })
      if (!response.ok && response.status !== 401) throw new Error()
      setCsrfToken('')
      setUser(null)
    } catch { setError('Abmelden fehlgeschlagen. Bitte erneut versuchen.') }
    finally { setPending(false) }
  }

  if (loading) return <p role="status">Anmeldung wird geprüft …</p>
  if (user) return <>
    <nav className="auth-bar" aria-label="Benutzerkonto">
      <span>Angemeldet als {user.username}</span>
      <button onClick={logout} disabled={pending}>Abmelden</button>
      {error && <p role="alert">{error}</p>}
    </nav>
    <App />
  </>
  return <main className="auth-login">
    <h1>PaperlessCheck</h1>
    <h2>Anmelden</h2>
    <form onSubmit={login}>
      <label htmlFor="username">Benutzername</label>
      <input id="username" autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} required disabled={pending} />
      <label htmlFor="password">Passwort</label>
      <input id="password" type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} required disabled={pending} />
      <button disabled={pending}>{pending ? 'Anmeldung läuft …' : 'Anmelden'}</button>
    </form>
    {error && <p role="alert">{error}</p>}
    <p>Ein Konto erhältst du von der Administration dieser Instanz.</p>
  </main>
}

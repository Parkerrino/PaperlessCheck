// @vitest-environment jsdom
import React from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import AuthGate from './AuthGate'
vi.mock('./App', () => ({ default: () => <p>Geschützter Arbeitsbereich</p> }))
afterEach(() => { cleanup(); vi.unstubAllGlobals() })
const response = (status, data) => ({ status, ok: status === 200, json: async () => data })
describe('Anmeldung', () => {
  it('shows login, signs in and revokes the session on logout', async () => {
    const fetch = vi.fn().mockResolvedValueOnce(response(401, {}))
      .mockResolvedValueOnce(response(200, { user: { username: 'admin' }, csrf_token: 'csrf' }))
      .mockResolvedValueOnce(response(200, {}))
    vi.stubGlobal('fetch', fetch)
    render(<AuthGate />)
    fireEvent.change(await screen.findByLabelText('Benutzername'), { target: { value: 'admin' } })
    fireEvent.change(screen.getByLabelText('Passwort'), { target: { value: 'test password' } })
    fireEvent.click(screen.getByRole('button', { name: 'Anmelden' }))
    await screen.findByText('Geschützter Arbeitsbereich')
    expect(fetch.mock.calls[1][1].headers['X-Paperless-Login']).toBe('1')
    fireEvent.click(screen.getByRole('button', { name: 'Abmelden' }))
    await screen.findByLabelText('Benutzername')
    expect(fetch.mock.calls[2][1].headers['X-CSRF-Token']).toBe('csrf')
  })
  it('keeps the workspace hidden on a rejected login', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response(401, {})))
    render(<AuthGate />)
    fireEvent.change(await screen.findByLabelText('Benutzername'), { target: { value: 'admin' } })
    fireEvent.change(screen.getByLabelText('Passwort'), { target: { value: 'wrong' } })
    fireEvent.click(screen.getByRole('button', { name: 'Anmelden' }))
    await screen.findByRole('alert')
    expect(screen.queryByText('Geschützter Arbeitsbereich')).toBeNull()
    await waitFor(() => expect(screen.getByLabelText('Passwort').value).toBe(''))
  })
})

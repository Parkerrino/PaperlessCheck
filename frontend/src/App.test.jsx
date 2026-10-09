// @vitest-environment jsdom
import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import App from './App'

const list = { id: 1, title: 'Arbeitsbeginn', description: 'Vorbereitung', items: [
  { id: 2, title: 'Werkzeug prüfen', completed: false, order_index: 1 }
] }
const ok = data => Promise.resolve({ ok: true, json: async () => data })

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn().mockImplementation(() => ok([list])))
})
afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

async function ready() {
  render(<App />)
  await screen.findByRole('button', { name: /Arbeitsbeginn.*Aufgaben erledigt/ })
}

describe('Deutsche Oberfläche und sichere Bedienung', () => {
  it('unterscheidet fehlgeschlagenes Laden von einer leeren Sammlung', async () => {
    fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))
    render(<App />)
    expect((await screen.findByRole('alert')).textContent).toContain('konnten nicht geladen werden')
    expect(screen.queryByText(/Noch keine Checklisten vorhanden/)).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Aktualisieren' }))
    await screen.findByRole('button', { name: /Arbeitsbeginn.*Aufgaben erledigt/ })
  })

  it('setzt die Suche zurück und stellt den Fokus wieder her', async () => {
    await ready()
    fireEvent.change(screen.getByLabelText('Checklisten durchsuchen'), { target: { value: 'unbekannt' } })
    expect(screen.getByText(/Keine passenden Checklisten/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Suche zurücksetzen' }))
    expect(screen.getByLabelText('Checklisten durchsuchen').value).toBe('')
    expect(document.activeElement).toBe(screen.getByLabelText('Checklisten durchsuchen'))
  })

  it('sendet beim Abbrechen der Löschbestätigung keinen DELETE', async () => {
    await ready()
    const confirm = vi.spyOn(window, 'confirm').mockReturnValue(false)
    fireEvent.click(screen.getByRole('button', { name: 'Checkliste „Arbeitsbeginn“ löschen' }))
    expect(confirm).toHaveBeenCalledWith(expect.stringContaining('Alle zugehörigen Aufgaben'))
    expect(fetch).toHaveBeenCalledTimes(1)
  })

  it('behält die Checkliste bei einem fehlgeschlagenen DELETE', async () => {
    await ready()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    fetch.mockResolvedValueOnce({ ok: false })
    fireEvent.click(screen.getByRole('button', { name: 'Checkliste „Arbeitsbeginn“ löschen' }))
    await screen.findByRole('alert')
    expect(screen.getByRole('button', { name: 'Checkliste „Arbeitsbeginn“ löschen' })).toBeTruthy()
  })

  it('entfernt eine bestätigte Checkliste nach erfolgreichem DELETE', async () => {
    await ready()
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    fetch.mockImplementationOnce(() => ok({ message: 'deleted' }))
    fireEvent.click(screen.getByRole('button', { name: 'Checkliste „Arbeitsbeginn“ löschen' }))
    await screen.findByText('Die Checkliste „Arbeitsbeginn“ wurde gelöscht.')
    expect(screen.queryByRole('button', { name: 'Checkliste „Arbeitsbeginn“ löschen' })).toBeNull()
    expect(fetch.mock.calls[1][1].method).toBe('DELETE')
  })

  it('sendet bei wiederholtem Absenden nur einen POST und behält Eingaben bei Fehlern', async () => {
    await ready()
    let rejectRequest
    fetch.mockImplementationOnce(() => new Promise((resolve, reject) => { rejectRequest = reject }))
    const title = screen.getByLabelText('Titel der Checkliste')
    fireEvent.change(title, { target: { value: 'Neue Liste' } })
    const form = title.closest('form')
    fireEvent.submit(form)
    fireEvent.submit(form)
    expect(fetch).toHaveBeenCalledTimes(2)
    expect(screen.getByRole('button', { name: 'Wird angelegt …' }).disabled).toBe(true)
    rejectRequest(new TypeError('Failed to fetch'))
    await screen.findByRole('alert')
    expect(title.value).toBe('Neue Liste')
    expect(screen.getByRole('button', { name: 'Checkliste anlegen' }).disabled).toBe(false)
  })

  it('öffnet eine neu angelegte Checkliste und setzt Suchfilter zurück', async () => {
    await ready()
    fireEvent.change(screen.getByLabelText('Checklisten durchsuchen'), { target: { value: 'Vorbereitung' } })
    fireEvent.change(screen.getByLabelText('Titel der Checkliste'), { target: { value: '  Feierabend  ' } })
    fetch.mockImplementationOnce(() => ok({ id: 3, title: 'Feierabend', description: '' }))
    fireEvent.click(screen.getByRole('button', { name: 'Checkliste anlegen' }))
    await screen.findByRole('heading', { name: 'Feierabend' })
    expect(screen.getByLabelText('Checklisten durchsuchen').value).toBe('')
    expect(JSON.parse(fetch.mock.calls[1][1].body).title).toBe('Feierabend')
    expect(screen.getByRole('progressbar').value).toBe(0)
  })

  it('aktualisiert Aufgabenstatus und Fortschritt erst nach erfolgreicher Antwort', async () => {
    await ready()
    fetch.mockImplementationOnce(() => ok(list))
    fireEvent.click(screen.getByRole('button', { name: /Arbeitsbeginn.*Aufgaben erledigt/ }))
    const checkbox = await screen.findByRole('checkbox', { name: 'Werkzeug prüfen' })
    let resolveRequest
    fetch.mockImplementationOnce(() => new Promise(resolve => { resolveRequest = resolve }))
    fireEvent.click(checkbox)
    expect(checkbox.checked).toBe(false)
    resolveRequest({ ok: true, json: async () => ({ ...list.items[0], completed: true }) })
    await waitFor(() => expect(checkbox.checked).toBe(true))
    expect(screen.getByRole('progressbar').value).toBe(1)
  })
})

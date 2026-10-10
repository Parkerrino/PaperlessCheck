import React, { useEffect, useRef, useState } from 'react'
import './index.css'
import { filterChecklists } from './utils/filterChecklists'

import { API_BASE } from './utils/apiBase'

async function request(path = '', options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options)
  if (!response.ok) throw new Error('Die Anfrage ist fehlgeschlagen.')
  return response.json()
}

function jsonRequest(method, data) {
  return { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }
}

export default function App() {
  const [checklists, setChecklists] = useState([])
  const [selectedChecklist, setSelectedChecklist] = useState(null)
  const [newChecklistTitle, setNewChecklistTitle] = useState('')
  const [newChecklistDesc, setNewChecklistDesc] = useState('')
  const [newItemTitle, setNewItemTitle] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [pending, setPending] = useState('')
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [loaded, setLoaded] = useState(false)
  const actionLock = useRef(false)
  const searchInput = useRef(null)
  const itemInput = useRef(null)
  const busy = Boolean(pending)
  const filteredChecklists = filterChecklists(checklists, searchQuery)

  // The ref locks immediately, including repeated events before React renders.
  async function runAction(key, task, failureMessage, successMessage = '') {
    if (actionLock.current) return
    actionLock.current = true
    setPending(key)
    setError('')
    setNotice('')
    try {
      await task()
      setNotice(successMessage)
    } catch {
      setError(failureMessage)
    } finally {
      actionLock.current = false
      setPending('')
    }
  }

  function loadChecklists() {
    return runAction('load', async () => {
      const data = await request()
      if (!Array.isArray(data)) throw new Error('Ungültige Antwort')
      setChecklists(data)
      setSelectedChecklist(current => current
        ? data.find(list => list.id === current.id) || null
        : null)
      setLoaded(true)
    }, 'Die Checklisten konnten nicht geladen werden. Prüfe die Verbindung und versuche es erneut.')
  }

  useEffect(() => {
    void loadChecklists()
  }, [])

  function selectChecklist(id) {
    return runAction('detail', async () => {
      const data = await request(`/${id}`)
      setSelectedChecklist(data)
      setNewItemTitle('')
    }, 'Die Checkliste konnte nicht geöffnet werden. Bitte versuche es erneut.')
  }

  function updateItems(checklistId, transform) {
    const update = list => list.id === checklistId
      ? { ...list, items: transform(list.items || []) }
      : list
    setChecklists(current => current.map(update))
    setSelectedChecklist(current => current ? update(current) : null)
  }

  function createChecklist(event) {
    event.preventDefault()
    if (actionLock.current) return
    const title = newChecklistTitle.trim()
    if (!title) {
      setNotice('')
      setError('Bitte gib einen Titel für die Checkliste ein.')
      return
    }
    return runAction('create', async () => {
      const data = await request('', jsonRequest('POST', {
        title, description: newChecklistDesc.trim()
      }))
      const checklist = { ...data, items: data.items || [] }
      setChecklists(current => [checklist, ...current])
      setSelectedChecklist(checklist)
      setNewChecklistTitle('')
      setNewChecklistDesc('')
      setNewItemTitle('')
      setSearchQuery('')
    }, 'Die Checkliste konnte nicht angelegt oder die Antwort nicht empfangen werden. Deine Eingaben bleiben erhalten. Aktualisiere die Übersicht vor einem weiteren Versuch.',
    `Die Checkliste „${title}“ wurde angelegt.`)
  }

  function deleteChecklist(checklist) {
    if (actionLock.current) return
    if (!window.confirm(`Checkliste „${checklist.title}“ wirklich löschen?\n\nAlle zugehörigen Aufgaben werden ebenfalls gelöscht. Dies kann nicht rückgängig gemacht werden.`)) return
    return runAction('delete-list', async () => {
      await request(`/${checklist.id}`, { method: 'DELETE' })
      setChecklists(current => current.filter(list => list.id !== checklist.id))
      setSelectedChecklist(current => current?.id === checklist.id ? null : current)
      if (selectedChecklist?.id === checklist.id) setNewItemTitle('')
    }, 'Das Löschen konnte nicht bestätigt werden. Aktualisiere die Übersicht, um den aktuellen Stand zu prüfen.',
    `Die Checkliste „${checklist.title}“ wurde gelöscht.`)
  }

  async function addItem(event) {
    event.preventDefault()
    if (actionLock.current || !selectedChecklist) return
    const title = newItemTitle.trim()
    if (!title) {
      setNotice('')
      setError('Bitte gib einen Titel für die Aufgabe ein.')
      return
    }
    const checklistId = selectedChecklist.id
    const positions = (selectedChecklist.items || []).map(item =>
      Number.isInteger(item.order_index) ? item.order_index : 0)
    await runAction('add-item', async () => {
      const data = await request(`/${checklistId}/items`, jsonRequest('POST', {
        title, order_index: Math.max(0, ...positions) + 1
      }))
      updateItems(checklistId, items => [...items, data])
      setNewItemTitle('')
    }, 'Die Aufgabe konnte nicht angelegt oder die Antwort nicht empfangen werden. Deine Eingabe bleibt erhalten. Aktualisiere vor einem weiteren Versuch.',
    `Die Aufgabe „${title}“ wurde hinzugefügt.`)
    itemInput.current?.focus()
  }

  function toggleItem(item) {
    if (actionLock.current || !selectedChecklist) return
    const checklistId = selectedChecklist.id
    return runAction('toggle-item', async () => {
      const data = await request(`/items/${item.id}`, jsonRequest('PUT', {
        title: item.title, completed: !item.completed,
        order_index: item.order_index ?? 0
      }))
      updateItems(checklistId, items => items.map(current => current.id === item.id ? data : current))
    }, 'Der Aufgabenstatus konnte nicht gespeichert oder bestätigt werden. Aktualisiere die Übersicht, um den aktuellen Stand zu prüfen.',
    item.completed ? 'Die Aufgabe ist wieder offen.' : 'Die Aufgabe wurde als erledigt markiert.')
  }

  function deleteItem(item) {
    if (actionLock.current || !selectedChecklist) return
    if (!window.confirm(`Aufgabe „${item.title}“ wirklich löschen?\n\nDies kann nicht rückgängig gemacht werden.`)) return
    const checklistId = selectedChecklist.id
    return runAction('delete-item', async () => {
      await request(`/items/${item.id}`, { method: 'DELETE' })
      updateItems(checklistId, items => items.filter(current => current.id !== item.id))
    }, 'Das Löschen der Aufgabe konnte nicht bestätigt werden. Aktualisiere die Übersicht, um den aktuellen Stand zu prüfen.',
    `Die Aufgabe „${item.title}“ wurde gelöscht.`)
  }

  function clearSearch() {
    setSearchQuery('')
    searchInput.current?.focus()
  }

  const items = selectedChecklist?.items || []
  const completed = items.filter(item => item.completed).length

  return (
    <div className="App">
      <header className="App-header">
        <h1>📋 PaperlessCheck</h1>
        <p>Aufgaben organisieren. Gemeinsam den Überblick behalten.</p>
      </header>

      {error && <div className="error-message" role="alert">{error}</div>}
      <div className="feedback-region" role="status" aria-live="polite" aria-atomic="true">
        {busy ? <p className="status-message">{pending === 'load' || pending === 'detail'
          ? 'Daten werden geladen …' : 'Änderung wird gespeichert …'}</p>
          : notice && <p className="success-message">{notice}</p>}
      </div>

      <div className="container" aria-busy={busy}>
        <aside className="sidebar" aria-label="Checklistenübersicht">
          <div className="section-heading">
            <h2>Checklisten</h2>
            <button type="button" className="btn btn-secondary" disabled={busy}
              onClick={loadChecklists}>Aktualisieren</button>
          </div>
          <form onSubmit={createChecklist} className="create-form">
            <label htmlFor="checklist-title">Titel der Checkliste</label>
            <input id="checklist-title" className="input-field" placeholder="Zum Beispiel: Arbeitsbeginn"
              value={newChecklistTitle} maxLength={255} disabled={busy}
              onChange={event => setNewChecklistTitle(event.target.value)} />
            <label htmlFor="checklist-description">Beschreibung (optional)</label>
            <textarea id="checklist-description" className="input-field" rows="2"
              placeholder="Wofür ist diese Checkliste gedacht?" value={newChecklistDesc}
              disabled={busy} onChange={event => setNewChecklistDesc(event.target.value)} />
            <button type="submit" className="btn btn-primary" disabled={busy || !loaded || !newChecklistTitle.trim()}>
              {pending === 'create' ? 'Wird angelegt …' : 'Checkliste anlegen'}
            </button>
          </form>

          <div className="checklist-search">
            <label htmlFor="checklist-search">Checklisten durchsuchen</label>
            <input id="checklist-search" ref={searchInput} type="search" className="input-field"
              placeholder="Titel oder Beschreibung suchen …" value={searchQuery}
              onChange={event => setSearchQuery(event.target.value)} />
            {searchQuery && <button type="button" className="btn btn-secondary" onClick={clearSearch}>Suche zurücksetzen</button>}
            {loaded && <p className="search-summary">{filteredChecklists.length} von {checklists.length} Checklisten</p>}
          </div>

          <div className="checklists-list">
            {!loaded ? <p className="empty-state">{busy ? 'Checklisten werden geladen …' : 'Keine Daten geladen. Bitte erneut aktualisieren.'}</p>
              : checklists.length === 0 ? <p className="empty-state">Noch keine Checklisten vorhanden. Lege deine erste Checkliste an.</p>
                : filteredChecklists.length === 0 ? <p className="empty-state">Keine passenden Checklisten gefunden. Versuche einen anderen Suchbegriff.</p>
                  : filteredChecklists.map(checklist => (
                    <div key={checklist.id} className={`checklist-item ${selectedChecklist?.id === checklist.id ? 'active' : ''}`}>
                      <button type="button" className="checklist-title-btn" disabled={busy}
                        aria-pressed={selectedChecklist?.id === checklist.id} onClick={() => selectChecklist(checklist.id)}>
                        <span>{checklist.title}</span>
                        <span className="item-count" aria-label={`${(checklist.items || []).filter(item => item.completed).length} von ${checklist.items?.length || 0} Aufgaben erledigt`}>
                          {(checklist.items || []).filter(item => item.completed).length}/{checklist.items?.length || 0}
                        </span>
                      </button>
                      <button type="button" className="btn-delete" disabled={busy}
                        title={`Checkliste „${checklist.title}“ löschen`} aria-label={`Checkliste „${checklist.title}“ löschen`}
                        onClick={() => deleteChecklist(checklist)}>🗑️</button>
                    </div>
                  ))}
          </div>
        </aside>

        <main className="main-content">
          {selectedChecklist ? <div className="checklist-detail">
            <h2>{selectedChecklist.title}</h2>
            {selectedChecklist.description && <p className="description">{selectedChecklist.description}</p>}
            <p className="progress-summary">{completed} von {items.length} Aufgaben erledigt</p>
            <progress max={Math.max(items.length, 1)} value={completed} aria-label="Fortschritt der Checkliste" />
            <form onSubmit={addItem} className="add-item-form">
              <div className="item-input-group">
                <label htmlFor="item-title">Neue Aufgabe</label>
                <input id="item-title" ref={itemInput} className="input-field" placeholder="Was ist zu tun?"
                  value={newItemTitle} maxLength={255} disabled={busy}
                  onChange={event => setNewItemTitle(event.target.value)} />
              </div>
              <button type="submit" className="btn btn-primary" disabled={busy || !newItemTitle.trim()}>
                {pending === 'add-item' ? 'Wird hinzugefügt …' : 'Aufgabe hinzufügen'}
              </button>
            </form>
            <div className="items-list">
              <h3>Aufgaben</h3>
              {items.length > 0 ? <ul>{items.map(item => (
                <li key={item.id} className={item.completed ? 'completed' : ''}>
                  <label>
                    <input type="checkbox" checked={Boolean(item.completed)} disabled={busy} onChange={() => toggleItem(item)} />
                    <span>{item.title}</span>
                  </label>
                  <button type="button" className="btn-delete" disabled={busy}
                    title={`Aufgabe „${item.title}“ löschen`} aria-label={`Aufgabe „${item.title}“ löschen`}
                    onClick={() => deleteItem(item)}>🗑️</button>
                </li>
              ))}</ul> : <p className="empty-state">Diese Checkliste enthält noch keine Aufgaben.</p>}
            </div>
          </div> : <div className="empty-state-large"><p>Wähle eine Checkliste aus oder lege eine neue an.</p></div>}
        </main>
      </div>
    </div>
  )
}

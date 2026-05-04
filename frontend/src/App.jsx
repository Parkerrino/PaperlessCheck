import React, { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [checklists, setChecklists] = useState([])
  const [selectedChecklist, setSelectedChecklist] = useState(null)
  const [newChecklistTitle, setNewChecklistTitle] = useState('')
  const [newChecklistDesc, setNewChecklistDesc] = useState('')
  const [newItemTitle, setNewItemTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const API_BASE = 'http://localhost:5000/api/checklists'

  // Fetch all checklists on mount
  useEffect(() => {
    fetchChecklists()
  }, [])

  const fetchChecklists = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await fetch(API_BASE)
      if (!response.ok) throw new Error('Failed to fetch checklists')
      const data = await response.json()
      setChecklists(data || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchChecklistDetail = async (id) => {
    try {
      setError('')
      const response = await fetch(`${API_BASE}/${id}`)
      if (!response.ok) throw new Error('Failed to fetch checklist')
      const data = await response.json()
      setSelectedChecklist(data)
    } catch (err) {
      setError(err.message)
    }
  }

  const createChecklist = async (e) => {
    e.preventDefault()
    if (!newChecklistTitle.trim()) {
      setError('Checklist title is required')
      return
    }

    try {
      setError('')
      const response = await fetch(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newChecklistTitle,
          description: newChecklistDesc
        })
      })
      if (!response.ok) throw new Error('Failed to create checklist')
      
      setNewChecklistTitle('')
      setNewChecklistDesc('')
      await fetchChecklists()
    } catch (err) {
      setError(err.message)
    }
  }

  const deleteChecklist = async (id) => {
    if (!window.confirm('Are you sure you want to delete this checklist?')) return

    try {
      setError('')
      const response = await fetch(`${API_BASE}/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Failed to delete checklist')
      
      if (selectedChecklist?.id === id) setSelectedChecklist(null)
      await fetchChecklists()
    } catch (err) {
      setError(err.message)
    }
  }

  const addItem = async (e) => {
    e.preventDefault()
    if (!selectedChecklist || !newItemTitle.trim()) {
      setError('Please select a checklist and enter an item title')
      return
    }

    try {
      setError('')
      const response = await fetch(`${API_BASE}/${selectedChecklist.id}/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newItemTitle,
          order_index: (selectedChecklist.items?.length || 0) + 1
        })
      })
      if (!response.ok) throw new Error('Failed to add item')
      
      setNewItemTitle('')
      await fetchChecklistDetail(selectedChecklist.id)
    } catch (err) {
      setError(err.message)
    }
  }

  const toggleItem = async (itemId, completed) => {
    const item = selectedChecklist.items.find(i => i.id === itemId)
    if (!item) return

    try {
      setError('')
      const response = await fetch(`${API_BASE}/items/${itemId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: item.title,
          completed: !completed,
          order_index: item.order_index
        })
      })
      if (!response.ok) throw new Error('Failed to update item')
      
      await fetchChecklistDetail(selectedChecklist.id)
    } catch (err) {
      setError(err.message)
    }
  }

  const deleteItem = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return

    try {
      setError('')
      const response = await fetch(`${API_BASE}/items/${itemId}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Failed to delete item')
      
      await fetchChecklistDetail(selectedChecklist.id)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>📋 PaperlessCheck</h1>
        <p>Organize your tasks with digital checklists</p>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="container">
        {/* Sidebar - Checklists List */}
        <aside className="sidebar">
          <h2>Checklists</h2>
          
          <form onSubmit={createChecklist} className="create-form">
            <input
              type="text"
              placeholder="Checklist title"
              value={newChecklistTitle}
              onChange={(e) => setNewChecklistTitle(e.target.value)}
              className="input-field"
            />
            <textarea
              placeholder="Description (optional)"
              value={newChecklistDesc}
              onChange={(e) => setNewChecklistDesc(e.target.value)}
              className="input-field"
              rows="2"
            />
            <button type="submit" className="btn btn-primary">
              ➕ New Checklist
            </button>
          </form>

          <div className="checklists-list">
            {loading ? (
              <p>Loading...</p>
            ) : checklists.length === 0 ? (
              <p className="empty-state">No checklists yet</p>
            ) : (
              checklists.map((checklist) => (
                <div
                  key={checklist.id}
                  className={`checklist-item ${selectedChecklist?.id === checklist.id ? 'active' : ''}`}
                >
                  <button
                    onClick={() => fetchChecklistDetail(checklist.id)}
                    className="checklist-title-btn"
                  >
                    {checklist.title}
                    <span className="item-count">
                      {checklist.items?.filter(i => i.completed).length}/{checklist.items?.length || 0}
                    </span>
                  </button>
                  <button
                    onClick={() => deleteChecklist(checklist.id)}
                    className="btn-delete"
                    title="Delete checklist"
                  >
                    🗑️
                  </button>
                </div>
              ))
            )}
          </div>
        </aside>

        {/* Main Content - Checklist Details */}
        <main className="main-content">
          {selectedChecklist ? (
            <div className="checklist-detail">
              <h2>{selectedChecklist.title}</h2>
              {selectedChecklist.description && (
                <p className="description">{selectedChecklist.description}</p>
              )}

              <form onSubmit={addItem} className="add-item-form">
                <input
                  type="text"
                  placeholder="Add new item..."
                  value={newItemTitle}
                  onChange={(e) => setNewItemTitle(e.target.value)}
                  className="input-field"
                />
                <button type="submit" className="btn btn-primary">
                  Add Item
                </button>
              </form>

              <div className="items-list">
                <h3>Items</h3>
                {selectedChecklist.items && selectedChecklist.items.length > 0 ? (
                  <ul>
                    {selectedChecklist.items.map((item) => (
                      <li key={item.id} className={item.completed ? 'completed' : ''}>
                        <label>
                          <input
                            type="checkbox"
                            checked={item.completed}
                            onChange={() => toggleItem(item.id, item.completed)}
                          />
                          <span>{item.title}</span>
                        </label>
                        <button
                          onClick={() => deleteItem(item.id)}
                          className="btn-delete"
                          title="Delete item"
                        >
                          🗑️
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="empty-state">No items yet</p>
                )}
              </div>
            </div>
          ) : (
            <div className="empty-state-large">
              <p>Select a checklist to get started</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
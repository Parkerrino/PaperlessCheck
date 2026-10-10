// API root, without /checklists. Relative paths use the frontend origin.
export function resolveApiBase(value = '') {
  const base = value.trim().replace(/\/+$/, '') || '/api'
  if (base.startsWith('/') && !base.startsWith('//') && !/[?#\\]/.test(base)) return base
  let url
  try { url = new URL(base) } catch { throw new Error('Ungültige API-Basis.') }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    throw new Error('Die API-Basis muss ein HTTP(S)-Endpunkt ohne Zugangsdaten, Query oder Fragment sein.')
  }
  return base
}

export const API_BASE = `${resolveApiBase(import.meta.env.VITE_API_BASE_URL)}/checklists`

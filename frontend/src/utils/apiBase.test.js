import { describe, expect, it } from 'vitest'
import { API_BASE, resolveApiBase } from './apiBase'

describe('API configuration', () => {
  it('defaults to the current origin', () => expect(API_BASE).toBe('/api/checklists'))
  it.each(['', '  ', undefined])('defaults %s to /api', value => expect(resolveApiBase(value)).toBe('/api'))
  it.each([[' /api/ ', '/api'], ['/internal/api///', '/internal/api'], ['https://example.test/api/', 'https://example.test/api']])('normalizes %s', (value, expected) => expect(resolveApiBase(value)).toBe(expected))
  it.each(['//example.test/api', 'ftp://example.test/api', 'https://user:secret@example.test/api', '/api?x=1', '/api#x', 'https://example.test/api?q=1', 'not-a-url'])('rejects %s', value => expect(() => resolveApiBase(value)).toThrow())
})

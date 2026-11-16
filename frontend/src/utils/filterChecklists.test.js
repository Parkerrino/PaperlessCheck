import { describe, expect, it } from 'vitest'
import { filterChecklists } from './filterChecklists.js'

const checklists = [
  {
    id: 1,
    title: 'Server Maintenance',
    description: 'Install security updates'
  },
  {
    id: 2,
    title: 'Shopping',
    description: 'Milk and bread'
  },
  {
    id: 3,
    title: 'Weekend Tasks'
  }
]

describe('filterChecklists', () => {
  it('finds matches in the title', () => {
    expect(filterChecklists(checklists, 'Maintenance')).toEqual([
      checklists[0]
    ])
  })

  it('finds matches in the description', () => {
    expect(filterChecklists(checklists, 'bread')).toEqual([
      checklists[1]
    ])
  })

  it('ignores letter case', () => {
    expect(filterChecklists(checklists, 'sErVeR')).toEqual([
      checklists[0]
    ])
  })

  it('ignores leading and trailing whitespace', () => {
    expect(filterChecklists(checklists, '  Shopping  ')).toEqual([
      checklists[1]
    ])
  })

  it('returns all checklists for an empty or whitespace-only query', () => {
    expect(filterChecklists(checklists, '')).toEqual(checklists)
    expect(filterChecklists(checklists, '   ')).toEqual(checklists)
  })

  it('returns an empty array when nothing matches', () => {
    expect(filterChecklists(checklists, 'xyz-not-found')).toEqual([])
  })

  it('handles missing and null descriptions', () => {
    const withoutDescriptions = [
      { id: 10, title: 'Backup' },
      { id: 11, title: 'Backup verification', description: null }
    ]

    expect(filterChecklists(withoutDescriptions, 'backup')).toEqual(
      withoutDescriptions
    )
    expect(filterChecklists(withoutDescriptions, 'missing')).toEqual([])
  })
})
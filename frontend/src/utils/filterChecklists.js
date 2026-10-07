export function filterChecklists(checklists, searchQuery) {
    const normalizedQuery = searchQuery.trim().toLowerCase()

    return checklists.filter((checklist) => 
    [checklist.title, checklist.description].some((value) =>
        (value ?? '').toLowerCase().includes(normalizedQuery)
        )
    )
}

export function sortChecklists(checklists, sortBy) {
  const sortedChecklists = [...checklists];

  switch (sortBy) {
  case 'title-asc':
  sortedChecklists.sort((a, b) =>
    a.title.localeCompare(b.title, 'de') || a.id - b.id
  );
  break;

case 'title-desc':
  sortedChecklists.sort((a, b) =>
    b.title.localeCompare(a.title, 'de') || a.id - b.id
  );
  break;
  return sortedChecklists;
}
}
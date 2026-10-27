let csrfToken = ''
export function setCsrfToken(value) { csrfToken = value }
export function sessionHeaders() { return { 'X-CSRF-Token': csrfToken } }

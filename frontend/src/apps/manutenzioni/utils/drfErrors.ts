/**
 * Utility per gestione errori DRF (Django REST Framework).
 */

/**
 * Estrae messaggio di errore da risposta DRF.
 * Gestisce i formati comuni:
 * - { detail: string } (errori generici)
 * - { field: ["error1", "error2"] } (errori di validazione per campo)
 * - string (risposta raw)
 * - HTML (Django debug page) -> fallback al messaggio di default
 *
 * @param err - Errore axios con response.data
 * @param defaultMsg - Messaggio di fallback se nessun errore trovato
 * @returns Stringa con messaggio di errore formattato
 */
export const extractErrorMessage = (err: any, defaultMsg: string): string => {
  const data = err.response?.data;

  // Risposta stringa diretta
  if (typeof data === 'string') {
    // Rileva HTML (Django debug page o errori server)
    // Ritorna il messaggio di default invece di mostrare HTML
    if (data.includes('<!DOCTYPE') || data.includes('<html') || data.includes('<tr>')) {
      console.error('Server returned HTML error page:', data.substring(0, 500));
      return defaultMsg;
    }
    return data;
  }

  // Errore con campo detail (es. { detail: "Not found" })
  if (data?.detail) return data.detail;

  // Errori di validazione per campo (es. { fk_hr: ["Questo campo è richiesto."] })
  if (data && typeof data === 'object') {
    const errors = Object.entries(data)
      .map(([field, msgs]) => {
        const msgList = Array.isArray(msgs) ? msgs.join(', ') : String(msgs);
        return `${field}: ${msgList}`;
      })
      .join('; ');
    if (errors) return errors;
  }

  return defaultMsg;
};

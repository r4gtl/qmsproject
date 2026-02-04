/**
 * Utility per gestione errori DRF (Django REST Framework).
 */

/**
 * Estrae messaggio di errore da risposta DRF.
 * Gestisce i formati comuni:
 * - { detail: string } (errori generici)
 * - { field: ["error1", "error2"] } (errori di validazione per campo)
 * - string (risposta raw)
 *
 * @param err - Errore axios con response.data
 * @param defaultMsg - Messaggio di fallback se nessun errore trovato
 * @returns Stringa con messaggio di errore formattato
 */
export const extractErrorMessage = (err: any, defaultMsg: string): string => {
  const data = err.response?.data;

  // Risposta stringa diretta
  if (typeof data === 'string') return data;

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

/**
 * Normalizza input ore per formato italiano/internazionale.
 *
 * Gestisce:
 * - Formato italiano: "3,5" -> "3.5", "1.234,50" -> "1234.50"
 * - Formato internazionale: "1234.50" -> "1234.50"
 * - Spazi: " 2 345,00 " -> "2345.00"
 *
 * @param val - Stringa input dall'utente
 * @returns Stringa normalizzata con punto decimale, oppure null se invalida/vuota
 */
export const parseOreOrNull = (val: string): string | null => {
  if (!val || val.trim() === '') return null;

  let normalized: string;

  if (val.includes(',')) {
    // Formato italiano: rimuovi spazi e punti (migliaia), sostituisci virgola con punto
    normalized = val
      .replace(/\s/g, '')   // rimuovi spazi
      .replace(/\./g, '')   // rimuovi punti (separatore migliaia)
      .replace(',', '.');   // virgola -> punto decimale
  } else {
    // Formato internazionale: rimuovi solo spazi
    normalized = val.replace(/\s/g, '');
  }

  // Valida che sia un numero
  const parsed = Number(normalized);
  if (isNaN(parsed)) return null;

  // Ritorna la stringa normalizzata (DRF accetta string per DecimalField)
  return normalized;
};

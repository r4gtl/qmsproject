/**
 * API Client per Formazione
 *
 * CONFIGURAZIONE ENDPOINT LOOKUP:
 * Se gli endpoint dei lookup differiscono, modifica le costanti qui sotto.
 */
import instance from '@/api/axios';
import type {
  CorsoFormazione,
  RegistroFormazioneList,
  RegistroFormazioneDetail,
  RegistroFormazioneCreate,
  DettaglioRegistroFormazione,
  DettaglioRegistroFormazioneCreate,
  Fornitore,
} from '../types';
import type { PaginatedResponse, HumanResourceList } from '../../types';

// =============================================================================
// CONFIGURAZIONE ENDPOINT (modifica qui se differiscono)
// =============================================================================
const BASE_URL = '/human-resources';

/** Endpoint per lookup dipendenti. Modifica se diverso (es. '/human-resources/hr/') */
const HR_LOOKUP_URL = `${BASE_URL}/dipendenti/`;

/** Endpoint per lookup fornitori. Modifica se diverso */
const FORNITORI_LOOKUP_URL = '/anagrafiche/fornitori/';

// =============================================================================
// CORSI FORMAZIONE
// =============================================================================

/**
 * Lista corsi formazione.
 */
export const getCorsiFormazione = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<CorsoFormazione>>(`${BASE_URL}/corsi-formazione/`, { params });

// =============================================================================
// REGISTRI FORMAZIONE
// =============================================================================

/**
 * Lista registri formazione (dashboard).
 */
export const getRegistriFormazione = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<RegistroFormazioneList>>(`${BASE_URL}/registri-formazione/`, { params });

/**
 * Dettaglio registro formazione (con dettagli operatori).
 */
export const getRegistroFormazione = (id: number) =>
  instance.get<RegistroFormazioneDetail>(`${BASE_URL}/registri-formazione/${id}/`);

/**
 * Crea nuovo registro formazione.
 */
export const createRegistroFormazione = (data: RegistroFormazioneCreate) =>
  instance.post<RegistroFormazioneDetail>(`${BASE_URL}/registri-formazione/`, data);

/**
 * Aggiorna registro formazione.
 */
export const updateRegistroFormazione = (id: number, data: Partial<RegistroFormazioneCreate>) =>
  instance.patch<RegistroFormazioneDetail>(`${BASE_URL}/registri-formazione/${id}/`, data);

/**
 * Elimina registro formazione.
 */
export const deleteRegistroFormazione = (id: number) =>
  instance.delete(`${BASE_URL}/registri-formazione/${id}/`);

// =============================================================================
// DETTAGLI FORMAZIONE (OPERATORI)
// =============================================================================

/**
 * Dettaglio singolo dettaglio formazione.
 */
export const getDettaglioFormazione = (id: number) =>
  instance.get<DettaglioRegistroFormazione>(`${BASE_URL}/dettagli-formazione/${id}/`);

/**
 * Crea nuovo dettaglio formazione (JSON o FormData per upload).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 * Il browser genera automaticamente il boundary corretto.
 * L'interceptor axios aggiunge Authorization header.
 */
export const createDettaglioFormazione = (data: DettaglioRegistroFormazioneCreate | FormData) =>
  instance.post<DettaglioRegistroFormazione>(`${BASE_URL}/dettagli-formazione/`, data);

/**
 * Aggiorna dettaglio formazione (JSON o FormData per upload).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 * Il browser genera automaticamente il boundary corretto.
 * L'interceptor axios aggiunge Authorization header.
 */
export const updateDettaglioFormazione = (
  id: number,
  data: Partial<DettaglioRegistroFormazioneCreate> | FormData
) => instance.patch<DettaglioRegistroFormazione>(`${BASE_URL}/dettagli-formazione/${id}/`, data);

/**
 * Elimina dettaglio formazione.
 */
export const deleteDettaglioFormazione = (id: number) =>
  instance.delete(`${BASE_URL}/dettagli-formazione/${id}/`);

// =============================================================================
// LOOKUP: DIPENDENTI (HR)
// =============================================================================

/**
 * Lista dipendenti per select.
 * Endpoint configurato in HR_LOOKUP_URL (default: /human-resources/dipendenti/)
 */
export const getDipendentiForSelect = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<HumanResourceList>>(HR_LOOKUP_URL, {
    params: { page_size: 1000, ...params },
  });

// =============================================================================
// LOOKUP: FORNITORI
// =============================================================================

/**
 * Lista fornitori per select.
 * Endpoint configurato in FORNITORI_LOOKUP_URL (default: /anagrafiche/fornitori/)
 */
export const getFornitoriForSelect = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Fornitore>>(FORNITORI_LOOKUP_URL, {
    params: { page_size: 1000, ...params },
  });

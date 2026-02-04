/**
 * API Client per Tabelle Formazione (Aree + Corsi)
 *
 * Endpoints:
 * - /api/human-resources/aree-formazione/
 * - /api/human-resources/corsi-formazione/
 */
import instance from '@/api/axios';
import type {
  AreaFormazione,
  AreaFormazioneCreate,
  CorsoFormazione,
  CorsoFormazioneCreate,
  PaginatedResponse,
} from '../types';

const BASE_URL = '/human-resources';

// =============================================================================
// AREE FORMAZIONE
// =============================================================================

/**
 * Lista aree formazione.
 * @param params - { page_size?: number }
 */
export const getAreeFormazione = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<AreaFormazione>>(`${BASE_URL}/aree-formazione/`, { params });

/**
 * Dettaglio area formazione.
 */
export const getAreaFormazione = (id: number) =>
  instance.get<AreaFormazione>(`${BASE_URL}/aree-formazione/${id}/`);

/**
 * Crea nuova area formazione.
 */
export const createAreaFormazione = (data: AreaFormazioneCreate) =>
  instance.post<AreaFormazione>(`${BASE_URL}/aree-formazione/`, data);

/**
 * Aggiorna area formazione.
 */
export const updateAreaFormazione = (id: number, data: Partial<AreaFormazioneCreate>) =>
  instance.patch<AreaFormazione>(`${BASE_URL}/aree-formazione/${id}/`, data);

/**
 * Elimina area formazione.
 */
export const deleteAreaFormazione = (id: number) =>
  instance.delete(`${BASE_URL}/aree-formazione/${id}/`);

// =============================================================================
// CORSI FORMAZIONE
// =============================================================================

/**
 * Lista corsi formazione.
 * @param params - { page_size?: number, fk_areaformazione?: number }
 */
export const getCorsiFormazione = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<CorsoFormazione>>(`${BASE_URL}/corsi-formazione/`, { params });

/**
 * Dettaglio corso formazione.
 */
export const getCorsoFormazione = (id: number) =>
  instance.get<CorsoFormazione>(`${BASE_URL}/corsi-formazione/${id}/`);

/**
 * Crea nuovo corso formazione.
 */
export const createCorsoFormazione = (data: CorsoFormazioneCreate) =>
  instance.post<CorsoFormazione>(`${BASE_URL}/corsi-formazione/`, data);

/**
 * Aggiorna corso formazione.
 */
export const updateCorsoFormazione = (id: number, data: Partial<CorsoFormazioneCreate>) =>
  instance.patch<CorsoFormazione>(`${BASE_URL}/corsi-formazione/${id}/`, data);

/**
 * Elimina corso formazione.
 */
export const deleteCorsoFormazione = (id: number) =>
  instance.delete(`${BASE_URL}/corsi-formazione/${id}/`);

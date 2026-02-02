/**
 * API Client per Human Resources
 */
import instance from '@/api/axios';
import type {
  HumanResourceList,
  HumanResourceDetail,
  HumanResourceCreate,
  CentrodiLavoro,
  Ward,
  Role,
  ValutazioneOperatore,
  ValutazioneCreate,
  PaginatedResponse,
} from '../types';

const BASE_URL = '/human-resources';

// =============================================================================
// DIPENDENTI
// =============================================================================

/**
 * Lista dipendenti con ricerca e paginazione.
 * @param params - { q?: string, page?: number, page_size?: number, ordering?: string }
 */
export const getDipendenti = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<HumanResourceList>>(`${BASE_URL}/dipendenti/`, { params });

/**
 * Dettaglio dipendente.
 */
export const getDipendente = (id: number) =>
  instance.get<HumanResourceDetail>(`${BASE_URL}/dipendenti/${id}/`);

/**
 * Crea nuovo dipendente.
 */
export const createDipendente = (data: HumanResourceCreate) =>
  instance.post<HumanResourceDetail>(`${BASE_URL}/dipendenti/`, data);

/**
 * Aggiorna dipendente.
 */
export const updateDipendente = (id: number, data: Partial<HumanResourceCreate>) =>
  instance.patch<HumanResourceDetail>(`${BASE_URL}/dipendenti/${id}/`, data);

/**
 * Elimina dipendente.
 */
export const deleteDipendente = (id: number) =>
  instance.delete(`${BASE_URL}/dipendenti/${id}/`);

// =============================================================================
// CENTRI DI LAVORO
// =============================================================================

export const getCentriDiLavoro = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<CentrodiLavoro>>(`${BASE_URL}/centri-di-lavoro/`, { params });

export const getCentroDiLavoro = (id: number) =>
  instance.get<CentrodiLavoro>(`${BASE_URL}/centri-di-lavoro/${id}/`);

export const createCentroDiLavoro = (data: { description: string }) =>
  instance.post<CentrodiLavoro>(`${BASE_URL}/centri-di-lavoro/`, data);

export const updateCentroDiLavoro = (id: number, data: { description: string }) =>
  instance.patch<CentrodiLavoro>(`${BASE_URL}/centri-di-lavoro/${id}/`, data);

export const deleteCentroDiLavoro = (id: number) =>
  instance.delete(`${BASE_URL}/centri-di-lavoro/${id}/`);

// =============================================================================
// REPARTI (WARD)
// =============================================================================

export const getReparti = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Ward>>(`${BASE_URL}/reparti/`, { params });

export const getReparto = (id: number) =>
  instance.get<Ward>(`${BASE_URL}/reparti/${id}/`);

export const createReparto = (data: { description: string }) =>
  instance.post<Ward>(`${BASE_URL}/reparti/`, data);

export const updateReparto = (id: number, data: { description: string }) =>
  instance.patch<Ward>(`${BASE_URL}/reparti/${id}/`, data);

export const deleteReparto = (id: number) =>
  instance.delete(`${BASE_URL}/reparti/${id}/`);

// =============================================================================
// MANSIONI (ROLE)
// =============================================================================

export const getMansioni = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Role>>(`${BASE_URL}/mansioni/`, { params });

export const getMansione = (id: number) =>
  instance.get<Role>(`${BASE_URL}/mansioni/${id}/`);

export const createMansione = (data: { description: string; fk_reparto?: number | null }) =>
  instance.post<Role>(`${BASE_URL}/mansioni/`, data);

export const updateMansione = (id: number, data: { description?: string; fk_reparto?: number | null }) =>
  instance.patch<Role>(`${BASE_URL}/mansioni/${id}/`, data);

export const deleteMansione = (id: number) =>
  instance.delete(`${BASE_URL}/mansioni/${id}/`);

// =============================================================================
// VALUTAZIONI
// =============================================================================

/**
 * Lista valutazioni, filtrabile per fk_hr.
 */
export const getValutazioni = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<ValutazioneOperatore>>(`${BASE_URL}/valutazioni/`, { params });

export const getValutazione = (id: number) =>
  instance.get<ValutazioneOperatore>(`${BASE_URL}/valutazioni/${id}/`);

export const createValutazione = (data: ValutazioneCreate) =>
  instance.post<ValutazioneOperatore>(`${BASE_URL}/valutazioni/`, data);

export const updateValutazione = (id: number, data: Partial<ValutazioneCreate>) =>
  instance.patch<ValutazioneOperatore>(`${BASE_URL}/valutazioni/${id}/`, data);

export const deleteValutazione = (id: number) =>
  instance.delete(`${BASE_URL}/valutazioni/${id}/`);

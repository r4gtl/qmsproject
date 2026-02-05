/**
 * API Client per Acquisto Pelli
 */
import instance from '@/api/axios';
import type {
  PaginatedResponse,
  TipoAnimale, TipoGrezzo, Scelta,
  LwgRegione, LwgSubregione, Nazione,
  LottoList, LottoDetail, LottoCreate,
  SceltaLotto, SceltaLottoCreate,
  LottoOrigine, LottoOrigineCreate,
  Fornitore,
} from '../types';

const BASE = '/acquistopelli';

// =============================================================================
// TABELLE GENERICHE
// =============================================================================

// Tipi Animale
export const getTipiAnimale = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<TipoAnimale>>(`${BASE}/tipoanimali/`, { params });

export const createTipoAnimale = (data: { descrizione: string }) =>
  instance.post<TipoAnimale>(`${BASE}/tipoanimali/`, data);

export const updateTipoAnimale = (id: number, data: { descrizione: string }) =>
  instance.patch<TipoAnimale>(`${BASE}/tipoanimali/${id}/`, data);

export const deleteTipoAnimale = (id: number) =>
  instance.delete(`${BASE}/tipoanimali/${id}/`);

// Tipi Grezzo
export const getTipiGrezzo = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<TipoGrezzo>>(`${BASE}/tipogrezzi/`, { params });

export const createTipoGrezzo = (data: { descrizione: string }) =>
  instance.post<TipoGrezzo>(`${BASE}/tipogrezzi/`, data);

export const updateTipoGrezzo = (id: number, data: { descrizione: string }) =>
  instance.patch<TipoGrezzo>(`${BASE}/tipogrezzi/${id}/`, data);

export const deleteTipoGrezzo = (id: number) =>
  instance.delete(`${BASE}/tipogrezzi/${id}/`);

// Scelte
export const getScelte = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Scelta>>(`${BASE}/scelte/`, { params });

export const createScelta = (data: { descrizione: string }) =>
  instance.post<Scelta>(`${BASE}/scelte/`, data);

export const updateScelta = (id: number, data: { descrizione: string }) =>
  instance.patch<Scelta>(`${BASE}/scelte/${id}/`, data);

export const deleteScelta = (id: number) =>
  instance.delete(`${BASE}/scelte/${id}/`);

// =============================================================================
// REGIONI / SUBREGIONI / NAZIONI
// =============================================================================

export const getRegioni = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<LwgRegione>>(`${BASE}/regioni/`, { params });

export const createRegione = (data: Partial<LwgRegione>) =>
  instance.post<LwgRegione>(`${BASE}/regioni/`, data);

export const updateRegione = (id: number, data: Partial<LwgRegione>) =>
  instance.patch<LwgRegione>(`${BASE}/regioni/${id}/`, data);

export const deleteRegione = (id: number) =>
  instance.delete(`${BASE}/regioni/${id}/`);

export const getSubregioni = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<LwgSubregione>>(`${BASE}/subregioni/`, { params });

export const createSubregione = (data: Partial<LwgSubregione>) =>
  instance.post<LwgSubregione>(`${BASE}/subregioni/`, data);

export const updateSubregione = (id: number, data: Partial<LwgSubregione>) =>
  instance.patch<LwgSubregione>(`${BASE}/subregioni/${id}/`, data);

export const deleteSubregione = (id: number) =>
  instance.delete(`${BASE}/subregioni/${id}/`);

export const getNazioni = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Nazione>>(`${BASE}/nazioni/`, { params });

export const createNazione = (data: Partial<Nazione>) =>
  instance.post<Nazione>(`${BASE}/nazioni/`, data);

export const updateNazione = (id: number, data: Partial<Nazione>) =>
  instance.patch<Nazione>(`${BASE}/nazioni/${id}/`, data);

export const deleteNazione = (id: number) =>
  instance.delete(`${BASE}/nazioni/${id}/`);

// =============================================================================
// LOTTI
// =============================================================================

export const getLotti = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<LottoList>>(`${BASE}/lotti/`, { params });

export const getLotto = (id: number) =>
  instance.get<LottoDetail>(`${BASE}/lotti/${id}/`);

export const createLotto = (data: LottoCreate) =>
  instance.post<LottoDetail>(`${BASE}/lotti/`, data);

export const updateLotto = (id: number, data: Partial<LottoCreate>) =>
  instance.patch<LottoDetail>(`${BASE}/lotti/${id}/`, data);

export const deleteLotto = (id: number) =>
  instance.delete(`${BASE}/lotti/${id}/`);

// =============================================================================
// SCELTE LOTTO
// =============================================================================

export const getScelteLotto = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<SceltaLotto>>(`${BASE}/scelte-lotto/`, { params });

export const createSceltaLotto = (data: SceltaLottoCreate) =>
  instance.post<SceltaLotto>(`${BASE}/scelte-lotto/`, data);

export const updateSceltaLotto = (id: number, data: Partial<SceltaLottoCreate>) =>
  instance.patch<SceltaLotto>(`${BASE}/scelte-lotto/${id}/`, data);

export const deleteSceltaLotto = (id: number) =>
  instance.delete(`${BASE}/scelte-lotto/${id}/`);

// =============================================================================
// LOTTO ORIGINI
// =============================================================================

export const getLottoOrigini = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<LottoOrigine>>(`${BASE}/lotto-origini/`, { params });

export const createLottoOrigine = (data: LottoOrigineCreate) =>
  instance.post<LottoOrigine>(`${BASE}/lotto-origini/`, data);

export const updateLottoOrigine = (id: number, data: Partial<LottoOrigineCreate>) =>
  instance.patch<LottoOrigine>(`${BASE}/lotto-origini/${id}/`, data);

export const deleteLottoOrigine = (id: number) =>
  instance.delete(`${BASE}/lotto-origini/${id}/`);

// =============================================================================
// FORNITORI LOOKUP
// =============================================================================

export const getFornitoriLookup = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Fornitore>>('/anagrafiche/fornitori/', {
    params: { page_size: 1000, ...params },
  });

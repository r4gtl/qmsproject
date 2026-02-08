/**
 * API Client per Manutenzioni
 *
 * CONFIGURAZIONE ENDPOINT LOOKUP:
 * Se gli endpoint dei lookup differiscono, modifica le costanti qui sotto.
 */
import instance from '@/api/axios';
import type {
  AttrezzaturaList,
  AttrezzaturaDetail,
  AttrezzaturaCreate,
  ManutenzioneStraordinaria,
  ManutenzioneStraordinariaCreate,
  ManutenzioneOrdinaria,
  ManutenzioneOrdinariaCreate,
  Taratura,
  TaraturaCreate,
  ControlloPeriodico,
  ControlloPeriodicoCreate,
  PaginatedResponse,
  Ward,
  HumanResource,
  Fornitore,
} from '../types';

// =============================================================================
// CONFIGURAZIONE ENDPOINT (modifica qui se differiscono)
// =============================================================================
const BASE_URL = '/manutenzioni';

/** Endpoint per lookup reparti */
const WARD_LOOKUP_URL = '/human-resources/reparti/';

/** Endpoint per lookup dipendenti */
const HR_LOOKUP_URL = '/human-resources/dipendenti/';

/** Endpoint per lookup fornitori */
const FORNITORI_LOOKUP_URL = '/anagrafiche/fornitori/';

// =============================================================================
// ATTREZZATURE
// =============================================================================

/**
 * Lista attrezzature (con paginazione e ricerca).
 */
export const getAttrezzature = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<AttrezzaturaList>>(`${BASE_URL}/attrezzature/`, { params });

/**
 * Dettaglio attrezzatura.
 */
export const getAttrezzatura = (id: number) =>
  instance.get<AttrezzaturaDetail>(`${BASE_URL}/attrezzature/${id}/`);

/**
 * Crea nuova attrezzatura (JSON o FormData per upload image).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 * Il browser genera automaticamente il boundary corretto.
 * L'interceptor axios aggiunge Authorization header.
 */
export const createAttrezzatura = (data: AttrezzaturaCreate | FormData) =>
  instance.post<AttrezzaturaDetail>(`${BASE_URL}/attrezzature/`, data);

/**
 * Aggiorna attrezzatura (JSON o FormData per upload image).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 * Il browser genera automaticamente il boundary corretto.
 * L'interceptor axios aggiunge Authorization header.
 */
export const updateAttrezzatura = (id: number, data: Partial<AttrezzaturaCreate> | FormData) =>
  instance.patch<AttrezzaturaDetail>(`${BASE_URL}/attrezzature/${id}/`, data);

/**
 * Elimina attrezzatura.
 */
export const deleteAttrezzatura = (id: number) =>
  instance.delete(`${BASE_URL}/attrezzature/${id}/`);

// =============================================================================
// MANUTENZIONI STRAORDINARIE
// =============================================================================

/**
 * Lista manutenzioni straordinarie.
 */
export const getManutenzioniStraordinarie = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<ManutenzioneStraordinaria>>(
    `${BASE_URL}/manutenzioni-straordinarie/`,
    { params }
  );

/**
 * Dettaglio manutenzione straordinaria.
 */
export const getManutenzioneStraordinaria = (id: number) =>
  instance.get<ManutenzioneStraordinaria>(`${BASE_URL}/manutenzioni-straordinarie/${id}/`);

/**
 * Crea nuova manutenzione straordinaria.
 */
export const createManutenzioneStraordinaria = (data: ManutenzioneStraordinariaCreate) =>
  instance.post<ManutenzioneStraordinaria>(`${BASE_URL}/manutenzioni-straordinarie/`, data);

/**
 * Aggiorna manutenzione straordinaria.
 */
export const updateManutenzioneStraordinaria = (
  id: number,
  data: Partial<ManutenzioneStraordinariaCreate>
) =>
  instance.patch<ManutenzioneStraordinaria>(`${BASE_URL}/manutenzioni-straordinarie/${id}/`, data);

/**
 * Elimina manutenzione straordinaria.
 */
export const deleteManutenzioneStraordinaria = (id: number) =>
  instance.delete(`${BASE_URL}/manutenzioni-straordinarie/${id}/`);

// =============================================================================
// MANUTENZIONI ORDINARIE
// =============================================================================

/**
 * Lista manutenzioni ordinarie.
 */
export const getManutenzioniOrdinarie = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<ManutenzioneOrdinaria>>(`${BASE_URL}/manutenzioni-ordinarie/`, {
    params,
  });

/**
 * Dettaglio manutenzione ordinaria.
 */
export const getManutenzioneOrdinaria = (id: number) =>
  instance.get<ManutenzioneOrdinaria>(`${BASE_URL}/manutenzioni-ordinarie/${id}/`);

/**
 * Crea nuova manutenzione ordinaria.
 */
export const createManutenzioneOrdinaria = (data: ManutenzioneOrdinariaCreate) =>
  instance.post<ManutenzioneOrdinaria>(`${BASE_URL}/manutenzioni-ordinarie/`, data);

/**
 * Aggiorna manutenzione ordinaria.
 */
export const updateManutenzioneOrdinaria = (
  id: number,
  data: Partial<ManutenzioneOrdinariaCreate>
) => instance.patch<ManutenzioneOrdinaria>(`${BASE_URL}/manutenzioni-ordinarie/${id}/`, data);

/**
 * Elimina manutenzione ordinaria.
 */
export const deleteManutenzioneOrdinaria = (id: number) =>
  instance.delete(`${BASE_URL}/manutenzioni-ordinarie/${id}/`);

// =============================================================================
// TARATURE
// =============================================================================

/**
 * Lista tarature.
 */
export const getTarature = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Taratura>>(`${BASE_URL}/tarature/`, { params });

/**
 * Dettaglio taratura.
 */
export const getTaratura = (id: number) =>
  instance.get<Taratura>(`${BASE_URL}/tarature/${id}/`);

/**
 * Crea nuova taratura (JSON o FormData per upload documento).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 */
export const createTaratura = (data: TaraturaCreate | FormData) =>
  instance.post<Taratura>(`${BASE_URL}/tarature/`, data);

/**
 * Aggiorna taratura (JSON o FormData per upload documento).
 *
 * NOTA: NON settare Content-Type manualmente per FormData!
 */
export const updateTaratura = (id: number, data: Partial<TaraturaCreate> | FormData) =>
  instance.patch<Taratura>(`${BASE_URL}/tarature/${id}/`, data);

/**
 * Elimina taratura.
 */
export const deleteTaratura = (id: number) => instance.delete(`${BASE_URL}/tarature/${id}/`);

// =============================================================================
// CONTROLLI PERIODICI
// =============================================================================

/**
 * Lista controlli periodici.
 */
export const getControlliPeriodici = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<ControlloPeriodico>>(`${BASE_URL}/controlli-periodici/`, {
    params,
  });

/**
 * Dettaglio controllo periodico.
 */
export const getControlloPeriodico = (id: number) =>
  instance.get<ControlloPeriodico>(`${BASE_URL}/controlli-periodici/${id}/`);

/**
 * Crea nuovo controllo periodico.
 */
export const createControlloPeriodico = (data: ControlloPeriodicoCreate) =>
  instance.post<ControlloPeriodico>(`${BASE_URL}/controlli-periodici/`, data);

/**
 * Aggiorna controllo periodico.
 */
export const updateControlloPeriodico = (id: number, data: Partial<ControlloPeriodicoCreate>) =>
  instance.patch<ControlloPeriodico>(`${BASE_URL}/controlli-periodici/${id}/`, data);

/**
 * Elimina controllo periodico.
 */
export const deleteControlloPeriodico = (id: number) =>
  instance.delete(`${BASE_URL}/controlli-periodici/${id}/`);

// =============================================================================
// LOOKUP: REPARTI (WARD)
// =============================================================================

/**
 * Lista reparti per select.
 */
export const getWardsForSelect = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Ward>>(WARD_LOOKUP_URL, {
    params: { page_size: 1000, ...params },
  });

// =============================================================================
// LOOKUP: DIPENDENTI (HR)
// =============================================================================

/**
 * Lista dipendenti per select.
 */
export const getDipendentiForSelect = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<HumanResource>>(HR_LOOKUP_URL, {
    params: { page_size: 1000, ...params },
  });

// =============================================================================
// LOOKUP: FORNITORI
// =============================================================================

/**
 * Lista fornitori per select.
 */
export const getFornitoriForSelect = (params?: Record<string, unknown>) =>
  instance.get<PaginatedResponse<Fornitore>>(FORNITORI_LOOKUP_URL, {
    params: { page_size: 1000, ...params },
  });

/**
 * API per il Sistema Procedure
 */
import instance from '@/api/axios';
import type {
  Procedura,
  ProceduraDetail,
  ProceduraCreate,
  ProceduraUpdate,
  DettaglioProcedura,
  DettaglioProceduraCreate,
  DettaglioProceduraUpdate,
  CaratteristicaProcedura,
  CaratteristicaProceduraCreate,
  ReorderRequest,
  PaginatedResponse,
} from '../types/procedure';

// =============================================================================
// PROCEDURE
// =============================================================================

/**
 * Lista procedure per articolo
 */
export const getProcedureByArticolo = (articoloId: number) =>
  instance.get<PaginatedResponse<Procedura>>('/articoli/procedure/', {
    params: { fk_articolo: articoloId },
  });

/**
 * Dettaglio procedura con righe annidate
 */
export const getProcedura = (id: number) =>
  instance.get<ProceduraDetail>(`/articoli/procedure/${id}/`);

/**
 * Crea nuova revisione procedura
 */
export const createProcedura = (data: ProceduraCreate) =>
  instance.post<ProceduraDetail>('/articoli/procedure/', data);

/**
 * Aggiorna procedura (solo note e data_revisione)
 */
export const updateProcedura = (id: number, data: ProceduraUpdate) =>
  instance.patch<ProceduraDetail>(`/articoli/procedure/${id}/`, data);

/**
 * Elimina procedura
 */
export const deleteProcedura = (id: number) =>
  instance.delete(`/articoli/procedure/${id}/`);

/**
 * Clona procedura come nuova revisione
 */
export const cloneProcedura = (id: number, note?: string) =>
  instance.post<ProceduraDetail>(`/articoli/procedure/${id}/clone/`, { note });

/**
 * Riordina dettagli della procedura
 */
export const reorderDettagliProcedura = (
  proceduraId: number,
  orderedIds: number[]
) =>
  instance.post<DettaglioProcedura[]>(
    `/articoli/procedure/${proceduraId}/reorder-dettagli/`,
    { ordered_ids: orderedIds } as ReorderRequest
  );

// =============================================================================
// DETTAGLI PROCEDURA (Righe)
// =============================================================================

/**
 * Lista dettagli per procedura
 */
export const getDettagliByProcedura = (proceduraId: number) =>
  instance.get<PaginatedResponse<DettaglioProcedura>>(
    '/articoli/dettagli-procedura/',
    { params: { fk_procedura: proceduraId } }
  );

/**
 * Dettaglio singola riga
 */
export const getDettaglio = (id: number) =>
  instance.get<DettaglioProcedura>(`/articoli/dettagli-procedura/${id}/`);

/**
 * Crea nuova riga
 */
export const createDettaglio = (data: DettaglioProceduraCreate) =>
  instance.post<DettaglioProcedura>('/articoli/dettagli-procedura/', data);

/**
 * Aggiorna riga
 */
export const updateDettaglio = (id: number, data: DettaglioProceduraUpdate) =>
  instance.patch<DettaglioProcedura>(`/articoli/dettagli-procedura/${id}/`, data);

/**
 * Elimina riga
 */
export const deleteDettaglio = (id: number) =>
  instance.delete(`/articoli/dettagli-procedura/${id}/`);

/**
 * Riordina caratteristiche di un dettaglio
 */
export const reorderCaratteristiche = (
  dettaglioId: number,
  orderedIds: number[]
) =>
  instance.post<CaratteristicaProcedura[]>(
    `/articoli/dettagli-procedura/${dettaglioId}/reorder-caratteristiche/`,
    { ordered_ids: orderedIds } as ReorderRequest
  );

// =============================================================================
// CARATTERISTICHE PROCEDURA
// =============================================================================

/**
 * Lista caratteristiche per dettaglio
 */
export const getCaratteristicheByDettaglio = (dettaglioId: number) =>
  instance.get<PaginatedResponse<CaratteristicaProcedura>>(
    '/articoli/caratteristiche-procedura/',
    { params: { fk_dettaglio_procedura: dettaglioId } }
  );

/**
 * Crea nuova caratteristica
 */
export const createCaratteristica = (data: CaratteristicaProceduraCreate) =>
  instance.post<CaratteristicaProcedura>(
    '/articoli/caratteristiche-procedura/',
    data
  );

/**
 * Aggiorna caratteristica
 */
export const updateCaratteristica = (
  id: number,
  data: Partial<CaratteristicaProceduraCreate>
) =>
  instance.patch<CaratteristicaProcedura>(
    `/articoli/caratteristiche-procedura/${id}/`,
    data
  );

/**
 * Elimina caratteristica
 */
export const deleteCaratteristica = (id: number) =>
  instance.delete(`/articoli/caratteristiche-procedura/${id}/`);

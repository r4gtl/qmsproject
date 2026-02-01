/**
 * Types per il Sistema Procedure
 */

// =============================================================================
// CARATTERISTICA PROCEDURA
// =============================================================================

export interface CaratteristicaProcedura {
  id: number;
  fk_dettaglio_procedura: number;
  // Per lavorazione ESTERNA
  fk_fornitore: number | null;
  fk_fornitore_nome?: string;
  fk_lavorazione_esterna: number | null;
  fk_lavorazione_esterna_descrizione?: string;
  // Per lavorazione INTERNA
  fk_dettaglio_fase_lavoro: number | null;
  fk_dettaglio_fase_lavoro_attributo?: string;
  valore: string | null;
  note: string | null;
  numero_riga: number;
  created_by: number | null;
  created_at: string;
}

export interface CaratteristicaProceduraCreate {
  fk_dettaglio_procedura: number;
  fk_fornitore?: number | null;
  fk_lavorazione_esterna?: number | null;
  fk_dettaglio_fase_lavoro?: number | null;
  valore?: string;
  note?: string;
  numero_riga?: number;
}

// =============================================================================
// DETTAGLIO PROCEDURA (Riga)
// =============================================================================

export interface DettaglioProcedura {
  id: number;
  fk_procedura: number;
  fk_faselavoro: number;
  fk_faselavoro_descrizione?: string;
  fk_fornitore: number | null;
  fk_fornitore_nome?: string;
  is_interna: boolean;
  numero_riga: number;
  note: string | null;
  caratteristiche: CaratteristicaProcedura[];
  caratteristiche_count: number;
  created_by: number | null;
  created_at: string;
}

export interface DettaglioProceduraCreate {
  fk_procedura: number;
  fk_faselavoro: number;
  fk_fornitore?: number | null;
  is_interna: boolean;
  numero_riga?: number;
  note?: string;
}

export interface DettaglioProceduraUpdate {
  fk_faselavoro?: number;
  fk_fornitore?: number | null;
  is_interna?: boolean;
  note?: string;
}

// =============================================================================
// PROCEDURA
// =============================================================================

export interface Procedura {
  id: number;
  fk_articolo: number;
  fk_articolo_descrizione?: string;
  nr_procedura: number;
  data_procedura: string;
  nr_revisione: number;
  data_revisione: string;
  note: string | null;
  dettagli_count?: number;
  created_by: number | null;
  created_at: string;
}

export interface ProceduraDetail extends Procedura {
  dettagli: DettaglioProcedura[];
}

export interface ProceduraCreate {
  fk_articolo: number;
  note?: string;
  data_revisione?: string;
}

export interface ProceduraUpdate {
  note?: string;
  data_revisione?: string;
}

// =============================================================================
// REORDER
// =============================================================================

export interface ReorderRequest {
  ordered_ids: number[];
}

// =============================================================================
// API RESPONSES
// =============================================================================

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

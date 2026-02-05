/**
 * Types per Acquisto Pelli.
 *
 * NOTA: i campi DecimalField Django arrivano come string da DRF.
 */

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// =============================================================================
// TABELLE GENERICHE
// =============================================================================

export interface TipoAnimale {
  id: number;
  descrizione: string;
}

export interface TipoGrezzo {
  id: number;
  descrizione: string;
}

export interface Scelta {
  id: number;
  descrizione: string;
}

// =============================================================================
// LWG REGIONI / SUBREGIONI / NAZIONI
// =============================================================================

export interface LwgRegione {
  id: number;
  codice_m49: number | null;
  nome_regione: string;
}

export interface LwgSubregione {
  id: number;
  regione: number;
  regione_nome: string;
  codice_m49: number | null;
  nome_subregione: string;
}

export interface Nazione {
  id: number;
  sigla_estesa: string | null;
  descrizione: string | null;
  sigla: string | null;
  codice_m49: number | null;
  regione: number | null;
  regione_nome: string | null;
  subregione: number | null;
  subregione_nome: string | null;
}

// =============================================================================
// SCELTA LOTTO
// =============================================================================

export interface SceltaLotto {
  id: number;
  fk_lotto: number;
  fk_scelta: number;
  scelta_descrizione: string;
  pezzi: number | null;
  scelta_terminata: boolean;
  data_termine: string | null;
  note: string | null;
}

export interface SceltaLottoCreate {
  fk_lotto: number;
  fk_scelta: number;
  pezzi?: number | null;
  scelta_terminata?: boolean;
  data_termine?: string | null;
  note?: string | null;
}

// =============================================================================
// LOTTO ORIGINE
// =============================================================================

export interface LottoOrigine {
  id: number;
  lotto: number;
  nazione: number | null;
  nazione_display: string | null;
  regione: number | null;
  regione_display: string | null;
  subregione: number | null;
  subregione_display: string | null;
  quota_percentuale: string | null; // DecimalField
  qta_stimata: string | null; // DecimalField
  livello_rischio: string | null;
  fonte_dato: string | null;
  note: string | null;
  livello_precisione: 'country' | 'region' | 'subregion';
}

export interface LottoOrigineCreate {
  lotto: number;
  nazione?: number | null;
  regione?: number | null;
  subregione?: number | null;
  quota_percentuale?: string | null;
  qta_stimata?: string | null;
  livello_rischio?: string | null;
  fonte_dato?: string | null;
  note?: string | null;
  livello_precisione: 'country' | 'region' | 'subregion';
}

// =============================================================================
// LOTTO
// =============================================================================

export interface LottoList {
  id: number;
  data_acquisto: string;
  identificativo: string;
  fk_fornitore: number;
  fornitore_ragionesociale: string;
  fk_tipoanimale: number | null;
  tipoanimale_descrizione: string | null;
  fk_tipogrezzo: number | null;
  tipogrezzo_descrizione: string | null;
  origine: string | null;
  pezzi: number | null;
  peso_totale: string | null; // DecimalField
  is_lwg: boolean;
}

export interface LottoDetail {
  id: number;
  data_acquisto: string;
  identificativo: string;
  fk_fornitore: number;
  fornitore_ragionesociale: string;
  fk_tipoanimale: number | null;
  tipoanimale_descrizione: string | null;
  fk_tipogrezzo: number | null;
  tipogrezzo_descrizione: string | null;
  fk_macello: number | null;
  macello_ragionesociale: string | null;
  origine: string | null;
  documento: string | null;
  is_lwg: boolean;
  peso_totale: string | null;
  pezzi: number | null;
  prezzo_unitario: string | null;
  spese_accessorie: string | null;
  kg_km: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
  scelte: SceltaLotto[];
  origini: LottoOrigine[];
}

export interface LottoCreate {
  data_acquisto: string;
  identificativo: string;
  fk_fornitore: number;
  fk_tipoanimale?: number | null;
  fk_tipogrezzo?: number | null;
  fk_macello?: number | null;
  origine?: string | null;
  documento?: string | null;
  is_lwg?: boolean;
  peso_totale?: string | null;
  pezzi?: number | null;
  prezzo_unitario?: string | null;
  spese_accessorie?: string | null;
  kg_km?: string | null;
  note?: string | null;
}

// =============================================================================
// FORNITORE (per lookup select)
// =============================================================================

export interface Fornitore {
  id: number;
  ragionesociale: string;
}

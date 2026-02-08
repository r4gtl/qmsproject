/**
 * Types per Manutenzioni
 *
 * NOTA: I campi Decimal in Django (importo, ore_fermo) sono serializzati come string da DRF.
 * In frontend usiamo string | null e convertiamo solo per calcoli/display.
 */

// =============================================================================
// GENERIC
// =============================================================================

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// =============================================================================
// ATTREZZATURA
// =============================================================================

export interface AttrezzaturaList {
  id: number;
  codice_attrezzatura: string;
  descrizione: string;
  modello: string | null;
  fk_ward: number | null;
  fk_ward_display: string | null;
  fk_human_resource: number | null;
  fk_human_resource_display: string | null;
  is_dismesso: boolean;
  is_taratura: boolean;
}

export interface AttrezzaturaDetail {
  id: number;
  codice_attrezzatura: string;
  descrizione: string;
  modello: string | null;
  serie_matricola: string | null;
  fk_ward: number | null;
  fk_ward_display: string | null;
  is_dismesso: boolean;
  data_dismissione: string | null;
  is_taratura: boolean;
  periodo_taratura: number | null;
  procedura_controlli_periodici: string | null;
  periodo_controlli_periodici: number | null;
  riferimento_normativo_controlli_periodici: string | null;
  fk_human_resource: number | null;
  fk_human_resource_display: string | null;
  image: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
}

export interface AttrezzaturaCreate {
  codice_attrezzatura: string;
  descrizione: string;
  modello?: string | null;
  serie_matricola?: string | null;
  fk_ward?: number | null;
  is_dismesso?: boolean;
  data_dismissione?: string | null;
  is_taratura?: boolean;
  periodo_taratura?: number | null;
  procedura_controlli_periodici?: string | null;
  periodo_controlli_periodici?: number | null;
  riferimento_normativo_controlli_periodici?: string | null;
  fk_human_resource?: number | null;
  image?: File | null;
  note?: string | null;
}

// =============================================================================
// MANUTENZIONE STRAORDINARIA
// =============================================================================

export interface ManutenzioneStraordinaria {
  id: number;
  fk_attrezzatura: number;
  fk_attrezzatura_display: string;
  data_manutenzione: string;
  descrizione: string | null;
  importo: string | null; // DecimalField -> string
  ore_fermo: string | null; // DecimalField -> string
  fk_fornitore: number | null;
  fk_fornitore_display: string | null;
  ft_prot: string | null;
  data_fattura: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
}

export interface ManutenzioneStraordinariaCreate {
  fk_attrezzatura: number;
  data_manutenzione: string;
  descrizione?: string | null;
  importo?: string | null; // DecimalField -> string
  ore_fermo?: string | null; // DecimalField -> string
  fk_fornitore?: number | null;
  ft_prot?: string | null;
  data_fattura?: string | null;
  note?: string | null;
}

// =============================================================================
// MANUTENZIONE ORDINARIA
// =============================================================================

export interface ManutenzioneOrdinaria {
  id: number;
  fk_attrezzatura: number;
  fk_attrezzatura_display: string;
  data_manutenzione: string;
  descrizione: string | null;
  fk_fornitore: number | null;
  fk_fornitore_display: string | null;
  is_eseguita: boolean;
  prossima_scadenza: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
}

export interface ManutenzioneOrdinariaCreate {
  fk_attrezzatura: number;
  data_manutenzione: string;
  descrizione?: string | null;
  fk_fornitore?: number | null;
  is_eseguita?: boolean;
  prossima_scadenza?: string | null;
  note?: string | null;
}

// =============================================================================
// TARATURA
// =============================================================================

export interface Taratura {
  id: number;
  fk_attrezzatura: number;
  fk_attrezzatura_display: string;
  data_taratura: string;
  fk_fornitore: number | null;
  fk_fornitore_display: string | null;
  documento: string | null;
  documento_url: string | null;
  is_conforme: boolean;
  prossima_scadenza: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
}

export interface TaraturaCreate {
  fk_attrezzatura: number;
  data_taratura: string;
  fk_fornitore?: number | null;
  documento?: File | null;
  is_conforme?: boolean;
  prossima_scadenza?: string | null;
  note?: string | null;
}

// =============================================================================
// CONTROLLO PERIODICO
// =============================================================================

export interface ControlloPeriodico {
  id: number;
  fk_attrezzatura: number;
  fk_attrezzatura_display: string;
  data_controllo: string;
  descrizione: string | null;
  fk_human_resource: number | null;
  fk_human_resource_display: string | null;
  is_eseguita: boolean;
  prossima_scadenza: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string | null;
}

export interface ControlloPeriodicoCreate {
  fk_attrezzatura: number;
  data_controllo: string;
  descrizione?: string | null;
  fk_human_resource?: number | null;
  is_eseguita?: boolean;
  prossima_scadenza?: string | null;
  note?: string | null;
}

// =============================================================================
// LOOKUP TYPES (da altre app)
// =============================================================================

export interface Ward {
  id: number;
  description: string;
}

export interface HumanResource {
  id: number;
  cognomedipendente: string;
  nomedipendente: string;
  full_name?: string;
}

export interface Fornitore {
  id: number;
  ragionesociale: string;
}

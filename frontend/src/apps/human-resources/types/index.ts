/**
 * Types per Human Resources
 */

// =============================================================================
// CENTRO DI LAVORO
// =============================================================================

export interface CentrodiLavoro {
  id: number;
  description: string;
  created_at: string;
  updated_at: string;
}

// =============================================================================
// WARD (REPARTO)
// =============================================================================

export interface Ward {
  id: number;
  description: string;
  created_at: string;
  updated_at: string;
}

// =============================================================================
// ROLE (MANSIONE)
// =============================================================================

export interface Role {
  id: number;
  description: string;
  fk_reparto: number | null;
  fk_reparto_display: string | null;
  created_at: string;
  updated_at: string;
}

// =============================================================================
// SAFETY ROLE (INCARICHI SICUREZZA)
// =============================================================================

export interface SafetyRole {
  id: number;
  descrizione: string;
  note: string | null;
  created_at: string;
}

// =============================================================================
// HR SAFETY (INCARICHI SICUREZZA PER DIPENDENTE)
// =============================================================================

export interface HrSafety {
  id: number;
  fk_hr: number;
  fk_hr_display: string;
  fk_safety_role: number;
  fk_safety_role_display: string;
  data_inizio_incarico: string;
  data_fine_incarico: string | null;
  note: string | null;
  created_at: string;
}

export interface HrSafetyCreate {
  fk_hr: number;
  fk_safety_role: number;
  data_inizio_incarico: string;
  data_fine_incarico?: string | null;
  note?: string | null;
}

// =============================================================================
// HUMAN RESOURCE (DIPENDENTE)
// =============================================================================

export interface HumanResourceList {
  id: number;
  cognomedipendente: string;
  nomedipendente: string;
  full_name: string;
  dataassunzione: string;
  datadimissioni: string | null;
}

export interface HumanResourceDetail {
  id: number;
  cognomedipendente: string;
  nomedipendente: string;
  full_name: string;
  data_nascita: string | null;
  country: string | null;
  country_code: string | null;
  country_name: string | null;
  immagine: string | null;
  gender: 'M' | 'F' | null;
  contratto: 'determinato' | 'indeterminato' | null;
  orario: 'part_time' | 'full_time' | null;
  dataassunzione: string;
  datadimissioni: string | null;
  fk_mansione: number | null;
  fk_mansione_display: string | null;
  fk_reparto: number | null;
  fk_reparto_display: string | null;
  qualifica: string | null;
  commenti: string | null;
  created_at: string;
  updated_at: string;
}

export interface HumanResourceCreate {
  cognomedipendente: string;
  nomedipendente: string;
  data_nascita?: string | null;
  country?: string | null;
  gender?: 'M' | 'F' | null;
  contratto?: 'determinato' | 'indeterminato' | null;
  orario?: 'part_time' | 'full_time' | null;
  dataassunzione: string;
  datadimissioni?: string | null;
  fk_mansione?: number | null;
  fk_reparto?: number | null;
  qualifica?: string | null;
  commenti?: string | null;
}

// =============================================================================
// VALUTAZIONE OPERATORE
// =============================================================================

export type ValutazioneLevel = 'nessuna' | 'minimo' | 'medio' | 'migliore' | 'massimo';

export interface ValutazioneOperatore {
  id: number;
  fk_hr: number;
  fk_hr_display: string;
  fk_centro_di_lavoro: number;
  fk_centro_di_lavoro_display: string;
  valutazione: ValutazioneLevel;
  valutazione_display: string;
  note: string | null;
  created_at: string;
  updated_at: string;
}

export interface ValutazioneCreate {
  fk_hr: number;
  fk_centro_di_lavoro: number;
  valutazione: ValutazioneLevel;
  note?: string | null;
}

// =============================================================================
// PAGINATED RESPONSE
// =============================================================================

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// =============================================================================
// CHOICES
// =============================================================================

export const GENDER_CHOICES = [
  { value: 'M', label: 'Maschio' },
  { value: 'F', label: 'Femmina' },
];

export const CONTRATTO_CHOICES = [
  { value: 'determinato', label: 'Determinato' },
  { value: 'indeterminato', label: 'Indeterminato' },
];

export const ORARIO_CHOICES = [
  { value: 'part_time', label: 'Part-time' },
  { value: 'full_time', label: 'Full-time' },
];

export const VALUTAZIONE_CHOICES = [
  { value: 'nessuna', label: 'Nessuna Valutazione' },
  { value: 'minimo', label: 'Minimo - Richiede formazione approfondita' },
  { value: 'medio', label: 'Medio - Competente ma richiede affiancamento' },
  { value: 'migliore', label: 'Migliore - Sufficientemente competente' },
  { value: 'massimo', label: 'Massimo - Può formare altri operatori' },
];

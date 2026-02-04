/**
 * Types per Formazione
 *
 * NOTA: I campi "ore" sono DecimalField in Django - DRF li serializza come string.
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
// AREE FORMAZIONE
// =============================================================================

export interface AreaFormazione {
  id: number;
  descrizione: string;
  created_by: number | null;
}

export interface AreaFormazioneCreate {
  descrizione: string;
}

// =============================================================================
// CORSI FORMAZIONE
// =============================================================================

export interface CorsoFormazione {
  id: number;
  descrizione: string;
  fk_areaformazione: number;
  fk_areaformazione_display?: string; // Campo display, non sempre incluso nel serializer
  validita_mesi: number;
  created_by: number | null;
}

export interface CorsoFormazioneCreate {
  descrizione: string;
  fk_areaformazione: number;
  validita_mesi: number;
}

// =============================================================================
// REGISTRO FORMAZIONE (LIST / DASHBOARD)
// =============================================================================

export interface RegistroFormazioneList {
  id: number;
  data_formazione: string;
  fk_corso: number;
  corso_descrizione: string;
  fk_fornitore: number | null;
  fornitore_descrizione: string | null;
  ore: string | null; // DecimalField -> string
  num_partecipanti: number;
}

// =============================================================================
// DETTAGLIO REGISTRO FORMAZIONE
// =============================================================================

export interface DettaglioRegistroFormazione {
  id: number;
  fk_registro_formazione: number;
  fk_hr: number;
  fk_hr_display: string | null;
  ore: string | null; // DecimalField -> string
  note: string | null;
  certificato: string | null;
  certificato_url: string | null;
  presenza: 'presente' | 'assente';
  efficace: boolean;
  scadenza_calcolata: string | null;
  scadenza_override: string | null;
  scadenza_effettiva: string | null;
  created_by: number | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface DettaglioRegistroFormazioneCreate {
  fk_registro_formazione: number;
  fk_hr: number;
  ore?: string | null; // DecimalField -> string
  note?: string | null;
  certificato?: File | null;
  presenza: 'presente' | 'assente';
  efficace?: boolean;
  scadenza_override?: string | null;
}

// =============================================================================
// REGISTRO FORMAZIONE (DETAIL)
// =============================================================================

export interface RegistroFormazioneDetail {
  id: number;
  data_formazione: string;
  fk_corso: number;
  corso_descrizione: string;
  area_formazione?: string; // Può non essere presente
  validita_mesi?: number; // Può non essere presente
  fk_fornitore: number | null;
  fornitore_descrizione: string | null;
  ore: string | null; // DecimalField -> string
  note: string | null;
  created_by: number | null;
  dettagli: DettaglioRegistroFormazione[];
}

export interface RegistroFormazioneCreate {
  data_formazione: string;
  fk_corso: number;
  fk_fornitore?: number | null;
  ore?: string | null; // DecimalField -> string
  note?: string | null;
}

// =============================================================================
// FORNITORE (per select)
// =============================================================================

export interface Fornitore {
  id: number;
  ragionesociale: string;
}

// =============================================================================
// CHOICES
// =============================================================================

export const PRESENZA_CHOICES = [
  { value: 'presente', label: 'Presente' },
  { value: 'assente', label: 'Assente' },
];

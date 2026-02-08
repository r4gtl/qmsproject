/**
 * TypeScript types for Manuale Procedure API.
 */

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface SezioneLWG {
  id: number;
  lwgsection: string;
  note: string | null;
  created_by: number | null;
  created_at: string;
}

export interface Procedura {
  id: number;
  identificativo: string;
  data_procedura: string;
  descrizione: string;
  is_eliminata: boolean;
  fk_lwgsection: number | null;
  fk_lwgsection_display: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string;
}

export interface ProceduraCreate {
  identificativo: string;
  data_procedura: string;
  descrizione: string;
  is_eliminata?: boolean;
  fk_lwgsection?: number | null;
  note?: string;
}

export interface RevisioneProcedura {
  id: number;
  fk_procedura: number;
  fk_procedura_display: string;
  n_revisione: number;
  data_revisione: string;
  documento: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string;
}

export interface Modulo {
  id: number;
  fk_procedura: number;
  fk_procedura_display: string;
  identificativo: string;
  data_modulo: string;
  descrizione: string;
  note: string | null;
  created_by: number | null;
  created_at: string;
}

export interface RevisioneModulo {
  id: number;
  fk_modulo: number;
  fk_modulo_display: string;
  n_revisione: number;
  data_revisione: string;
  documento: string | null;
  note: string | null;
  created_by: number | null;
  created_at: string;
}

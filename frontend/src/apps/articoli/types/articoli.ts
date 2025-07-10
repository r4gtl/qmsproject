export interface Articolo {
  id: number;
  descrizione: string;
  scheda_tecnica?: string;
  industries_served?: string;
  fk_tipoanimale?: number;
  fk_tipogrezzo?: number;
  note?: string;
  created_at: string;
}

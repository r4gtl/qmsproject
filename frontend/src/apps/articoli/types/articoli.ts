export interface Articolo {
  id: number;
  descrizione: string;
  scheda_tecnica?: string;
  industries_served?: string;
  fk_tipoanimale?: number;
  fk_tipogrezzo?: number;
  fk_tipoanimale_descrizione?: string;
  fk_tipogrezzo_descrizione?: string;
  note?: string;
  created_at: string;
}

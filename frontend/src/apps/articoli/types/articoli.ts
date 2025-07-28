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

export interface ElencoTest {
  id: number;
  descrizione: string;
  norma_riferimento: string;
  note: string;
}

export interface FasiLavoro {
  id: number;
  descrizione: string;
  interno_esterno: string;
  um: string;
  note: string;
}

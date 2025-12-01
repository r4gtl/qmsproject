export interface Cliente {
  id?: number;
  ragionesociale: string;
  indirizzo?: string;
  telefono?: string;
  email?: string;
  partita_iva?: string;
  cap?: string;
  city?: string;
  provincia?: string;
  country: string;
  created_by?: number;
  created_at?: string;
}

export interface Fornitore {
  id: number;
  ragionesociale: string;
  country: string;
  categoria: string;
}

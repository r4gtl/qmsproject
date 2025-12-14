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

export interface LwgFornitore {
  id: number;
  lwg_urn: string;
  lwg_score: string;
  lwg_range: string | null;
  lwg_date: string | null;
  lwg_expiry: string | null;
  fk_fornitore: number;
}

export interface LwgCertificateTableProps {
  // ID del fornitore a cui appartengono i certificati LWG
  fornitoreId: number;
}

export interface Cliente {
  id: number;
  ragionesociale: string;
  indirizzo?: string;
  telefono?: string;
  email?: string;
  partita_iva?: string;
}

export interface Fornitore {
  id: number;
  ragionesociale: string;
  country: string;
  categoria: string;
}

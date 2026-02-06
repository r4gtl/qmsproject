// Type definitions for Monitoraggi module

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Monitoraggio Acqua
export interface MonitoraggioAcqua {
  id: number;
  data_lettura: string;
  mc_in: number;
  mc_out: number;
  note?: string;
  created_at: string;
}

// Monitoraggio Gas
export interface MonitoraggioGas {
  id: number;
  data_lettura: string;
  mc_in: string; // DecimalField as string
  note?: string;
  created_at: string;
}

// Monitoraggio Energia Elettrica
export interface MonitoraggioEnergiaElettrica {
  id: number;
  data_lettura: string;
  kwh_in: string; // DecimalField as string
  note?: string;
  created_at: string;
}

// Dato Produzione
export interface DatoProduzione {
  id: number;
  data_inserimento: string;
  industries_served: string;
  industries_served_display: string;
  fk_tipoanimale: number | null;
  tipoanimale_descrizione?: string;
  n_pelli: number;
  mq: string; // DecimalField as string
  kg?: string; // DecimalField as string, nullable
  note?: string;
  created_at: string;
}

// Form data types (for create/update - omit read-only fields)
export type MonitoraggioAcquaFormData = Omit<MonitoraggioAcqua, 'id' | 'created_at'>;
export type MonitoraggioGasFormData = Omit<MonitoraggioGas, 'id' | 'created_at'>;
export type MonitoraggioEnergiaElettricaFormData = Omit<MonitoraggioEnergiaElettrica, 'id' | 'created_at'>;
export type DatoProduzioneFormData = Omit<DatoProduzione, 'id' | 'created_at' | 'industries_served_display' | 'tipoanimale_descrizione'>;

import axios from '@/api/axios';
import type {
  MonitoraggioAcqua,
  MonitoraggioGas,
  MonitoraggioEnergiaElettrica,
  DatoProduzione,
  PaginatedResponse,
  MonitoraggioAcquaFormData,
  MonitoraggioGasFormData,
  MonitoraggioEnergiaElettricaFormData,
  DatoProduzioneFormData,
} from '../types';

const BASE_URL = '/monitoraggi';

// =============================================================================
// MONITORAGGIO ACQUA
// =============================================================================

export const getMonitoraggiAcqua = (params?: Record<string, unknown>) =>
  axios.get<PaginatedResponse<MonitoraggioAcqua>>(`${BASE_URL}/acqua/`, { params });

export const getMonitoraggioAcqua = (id: number) =>
  axios.get<MonitoraggioAcqua>(`${BASE_URL}/acqua/${id}/`);

export const createMonitoraggioAcqua = (data: MonitoraggioAcquaFormData) =>
  axios.post<MonitoraggioAcqua>(`${BASE_URL}/acqua/`, data);

export const updateMonitoraggioAcqua = (id: number, data: Partial<MonitoraggioAcquaFormData>) =>
  axios.patch<MonitoraggioAcqua>(`${BASE_URL}/acqua/${id}/`, data);

export const deleteMonitoraggioAcqua = (id: number) =>
  axios.delete(`${BASE_URL}/acqua/${id}/`);

// =============================================================================
// MONITORAGGIO GAS
// =============================================================================

export const getMonitoraggiGas = (params?: Record<string, unknown>) =>
  axios.get<PaginatedResponse<MonitoraggioGas>>(`${BASE_URL}/gas/`, { params });

export const getMonitoraggioGas = (id: number) =>
  axios.get<MonitoraggioGas>(`${BASE_URL}/gas/${id}/`);

export const createMonitoraggioGas = (data: MonitoraggioGasFormData) =>
  axios.post<MonitoraggioGas>(`${BASE_URL}/gas/`, data);

export const updateMonitoraggioGas = (id: number, data: Partial<MonitoraggioGasFormData>) =>
  axios.patch<MonitoraggioGas>(`${BASE_URL}/gas/${id}/`, data);

export const deleteMonitoraggioGas = (id: number) =>
  axios.delete(`${BASE_URL}/gas/${id}/`);

// =============================================================================
// MONITORAGGIO ENERGIA ELETTRICA
// =============================================================================

export const getMonitoraggiEnergiaElettrica = (params?: Record<string, unknown>) =>
  axios.get<PaginatedResponse<MonitoraggioEnergiaElettrica>>(`${BASE_URL}/energia-elettrica/`, { params });

export const getMonitoraggioEnergiaElettrica = (id: number) =>
  axios.get<MonitoraggioEnergiaElettrica>(`${BASE_URL}/energia-elettrica/${id}/`);

export const createMonitoraggioEnergiaElettrica = (data: MonitoraggioEnergiaElettricaFormData) =>
  axios.post<MonitoraggioEnergiaElettrica>(`${BASE_URL}/energia-elettrica/`, data);

export const updateMonitoraggioEnergiaElettrica = (id: number, data: Partial<MonitoraggioEnergiaElettricaFormData>) =>
  axios.patch<MonitoraggioEnergiaElettrica>(`${BASE_URL}/energia-elettrica/${id}/`, data);

export const deleteMonitoraggioEnergiaElettrica = (id: number) =>
  axios.delete(`${BASE_URL}/energia-elettrica/${id}/`);

// =============================================================================
// DATO PRODUZIONE
// =============================================================================

export const getDatiProduzione = (params?: Record<string, unknown>) =>
  axios.get<PaginatedResponse<DatoProduzione>>(`${BASE_URL}/dati-produzione/`, { params });

export const getDatoProduzione = (id: number) =>
  axios.get<DatoProduzione>(`${BASE_URL}/dati-produzione/${id}/`);

export const createDatoProduzione = (data: DatoProduzioneFormData) =>
  axios.post<DatoProduzione>(`${BASE_URL}/dati-produzione/`, data);

export const updateDatoProduzione = (id: number, data: Partial<DatoProduzioneFormData>) =>
  axios.patch<DatoProduzione>(`${BASE_URL}/dati-produzione/${id}/`, data);

export const deleteDatoProduzione = (id: number) =>
  axios.delete(`${BASE_URL}/dati-produzione/${id}/`);

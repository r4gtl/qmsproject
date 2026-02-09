/**
 * API client for Manuale Procedure endpoints.
 */
import instance from '@/api/axios';
import type {
  PaginatedResponse,
  SezioneLWG,
  Procedura,
  ProceduraCreate,
  RevisioneProcedura,
  Modulo,
  RevisioneModulo,
} from '../types';

const BASE_URL = '/manualeprocedure';

// =============================================================================
// SezioneLWG
// =============================================================================
export const getSezioniLWG = () =>
  instance.get<SezioneLWG[]>(`${BASE_URL}/sezioni-lwg/`);

// =============================================================================
// Procedura
// =============================================================================
export const getProcedure = (params?: Record<string, any>) =>
  instance.get<PaginatedResponse<Procedura>>(`${BASE_URL}/procedure/`, { params });

export const getProcedura = (id: number) =>
  instance.get<Procedura>(`${BASE_URL}/procedure/${id}/`);

export const createProcedura = (data: ProceduraCreate) =>
  instance.post<Procedura>(`${BASE_URL}/procedure/`, data);

export const updateProcedura = (id: number, data: Partial<ProceduraCreate>) =>
  instance.patch<Procedura>(`${BASE_URL}/procedure/${id}/`, data);

export const deleteProcedura = (id: number) =>
  instance.delete(`${BASE_URL}/procedure/${id}/`);

// =============================================================================
// RevisioneProcedura
// =============================================================================
export const getRevisioniProcedura = (params?: Record<string, any>) =>
  instance.get<PaginatedResponse<RevisioneProcedura>>(`${BASE_URL}/revisioni-procedure/`, { params });

export const createRevisioneProcedura = (data: FormData | any) =>
  instance.post<RevisioneProcedura>(`${BASE_URL}/revisioni-procedure/`, data);

export const updateRevisioneProcedura = (id: number, data: FormData | any) =>
  instance.patch<RevisioneProcedura>(`${BASE_URL}/revisioni-procedure/${id}/`, data);

export const deleteRevisioneProcedura = (id: number) =>
  instance.delete(`${BASE_URL}/revisioni-procedure/${id}/`);

// =============================================================================
// Modulo
// =============================================================================
export const getModuli = (params?: Record<string, any>) =>
  instance.get<PaginatedResponse<Modulo>>(`${BASE_URL}/moduli/`, { params });

export const getModulo = (id: number) =>
  instance.get<Modulo>(`${BASE_URL}/moduli/${id}/`);

export const createModulo = (data: any) =>
  instance.post<Modulo>(`${BASE_URL}/moduli/`, data);

export const updateModulo = (id: number, data: any) =>
  instance.patch<Modulo>(`${BASE_URL}/moduli/${id}/`, data);

export const deleteModulo = (id: number) =>
  instance.delete(`${BASE_URL}/moduli/${id}/`);

// =============================================================================
// RevisioneModulo
// =============================================================================
export const getRevisioniModulo = (params?: Record<string, any>) =>
  instance.get<PaginatedResponse<RevisioneModulo>>(`${BASE_URL}/revisioni-moduli/`, { params });

export const createRevisioneModulo = (data: FormData | any) =>
  instance.post<RevisioneModulo>(`${BASE_URL}/revisioni-moduli/`, data);

export const updateRevisioneModulo = (id: number, data: FormData | any) =>
  instance.patch<RevisioneModulo>(`${BASE_URL}/revisioni-moduli/${id}/`, data);

export const deleteRevisioneModulo = (id: number) =>
  instance.delete(`${BASE_URL}/revisioni-moduli/${id}/`);

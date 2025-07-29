import instance from '@/api/axios';
import type { Articolo, ElencoTest } from '@articoli/types/articoli';

export interface ArticoloFormData extends Omit<Articolo, 'id' | 'created_at'> {}

export const getArticoli = (params?: any) =>
  instance.get('/articoli/articoli/', { params });

export const getArticolo = (id: number) =>
  instance.get(`/articoli/articoli/${id}/`);

export const createArticolo = (data: FormData) =>
  instance.post('/articoli/articoli/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const updateArticolo = (id: number, data: FormData) =>
  instance.put(`/articoli/articoli/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const deleteArticolo = (id: number) =>
  instance.delete(`/articoli/articoli/${id}/`);

// Elenco Test

export const getTests = () => instance.get('/articoli/elenco-test/');

export const getTest = (id: number) =>
  instance.get(`/articoli/elenco-test/${id}/`);

export const createTest = (data: FormData) =>
  instance.post('/articoli/elenco-test/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const updateTest = (id: number, data: FormData) =>
  instance.put(`/articoli/elenco-test/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const deleteTest = (id: number) =>
  instance.delete(`/articoli/elenco-test/${id}/`);

// Fasi Lavoro

export const getFasi = () => instance.get('/articoli/fasi-lavoro/');

export const getFase = (id: number) =>
  instance.get(`/articoli/fasi-lavoro/${id}/`);

export const createFase = (data: FormData) =>
  instance.post('/articoli/fasi-lavoro/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const updateFase = (id: number, data: FormData) =>
  instance.put(`/articoli/fasi-lavoro/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

export const deleteFase = (id: number) =>
  instance.delete(`/articoli/fasi-lavoro/${id}/`);

// Dettaglio Fasi di Lavoro

export const getDettagliFase = (faseId: number) =>
  instance.get(`/articoli/fasi-lavoro-dettaglio/?fk_fase_lavoro=${faseId}`);

export const createDettaglioFase = (data: any) =>
  instance.post(`/articoli/fasi-lavoro-dettaglio/`, data);

export const updateDettaglioFase = (id: number, data: any) =>
  instance.put(`/articoli/fasi-lavoro-dettaglio/${id}/`, data);

export const deleteDettaglioFase = (id: number) =>
  instance.delete(`/articoli/fasi-lavoro-dettaglio/${id}/`);

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

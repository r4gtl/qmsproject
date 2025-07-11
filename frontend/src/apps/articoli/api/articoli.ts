import instance from '@/api/axios';
import type { Articolo } from '@articoli/types/articoli';

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

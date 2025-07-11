import axios from '../../../api/axios';

interface GetFornitoriParams {
  page?: number;
  search?: string;
  ordering?: string;
  categoria?: string;
  country?: string;
}

export const getClienti = () => axios.get('/api/anagrafiche/clienti/');
export const deleteFornitore = (id: number) =>
  axios.delete(`/api/anagrafiche/fornitori/${id}/`);

export function getFornitori(params: GetFornitoriParams = {}) {
  return axios.get('/api/anagrafiche/fornitori/', { params });
}

import axios from 'axios';

export const getClienti = () => axios.get('/anagrafiche/clienti/');
export const getFornitori = () => axios.get('/anagrafiche/fornitori/');
export const deleteFornitore = (id: number) =>
  axios.delete(`/anagrafiche/fornitori/${id}/`);

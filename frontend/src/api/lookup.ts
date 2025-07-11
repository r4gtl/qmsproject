import instance from '@/api/axios';

export const getTipoAnimali = () => instance.get('/tipoanimali/');
export const getTipoGrezzi = () => instance.get('/tipogrezzi/');

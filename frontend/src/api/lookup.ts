import instance from '@/api/axios';

export const getTipoAnimali = () => instance.get('/acquistopelli/tipoanimali/');
export const getTipoGrezzi = () => instance.get('/acquistopelli/tipogrezzi/');

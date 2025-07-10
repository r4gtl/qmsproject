import type { JSX } from 'react';
import { Navigate } from 'react-router-dom';

interface PrivateRouteProps {
  children: JSX.Element;
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
  const accessToken = localStorage.getItem('accessToken');

  return accessToken ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;

import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import Dashboard from './pages/Dashboard';
import PrivateRoute from './components/PrivateRoute';
import AppNavBar from './components/NavBar';

function App() {
  const location = useLocation();
  const isLoggedIn = !!localStorage.getItem('accessToken');
  const hideNavbar = location.pathname === '/login';

  return (
    <>
      {!hideNavbar && isLoggedIn && <AppNavBar />}
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </>
  );
}

export default App;

import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginForm from './components/auth/LoginForm';
import Dashboard from './pages/dashboard/Dashboard';
import PrivateRoute from './components/auth/PrivateRoute';
//import AppNavBar from './components/NavBar';
import Layout from './components/layout/Layout';
import FornitoriList from './apps/anagrafiche/pages/FornitoriList';
import FornitoreForm from './apps/anagrafiche/pages/FornitoreForm';
import ClientiList from './apps/anagrafiche/pages/ClientiList';
import ClienteForm from './apps/anagrafiche/pages/ClienteForm';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';

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

        <Route
          path="/fornitori"
          element={
            <PrivateRoute>
              <Layout>
                <FornitoriList />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/fornitori/nuovo/:categoria"
          element={
            <PrivateRoute>
              <Layout>
                <FornitoreForm mode="create" />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/fornitori/:id/modifica"
          element={
            <PrivateRoute>
              <Layout>
                <FornitoreForm mode="edit" />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/clienti"
          element={
            <PrivateRoute>
              <Layout>
                <ClientiList />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/clienti/nuovo"
          element={
            <PrivateRoute>
              <Layout>
                <ClienteForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/clienti/:id"
          element={
            <PrivateRoute>
              <Layout>
                <ClienteForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
      <ToastContainer position="top-right" autoClose={3000} />
    </>
  );
}

export default App;

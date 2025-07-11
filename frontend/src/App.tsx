import { Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/auth/LoginForm';
import Dashboard from '@/pages/dashboard/Dashboard';
import PrivateRoute from './components/auth/PrivateRoute';
import Layout from './components/layout/Layout';
import FornitoriList from '@anagrafiche/pages/FornitoriList';
import FornitoreForm from '@anagrafiche/pages/FornitoreForm';
import ClientiList from '@anagrafiche/pages/ClientiList';
import ClienteForm from '@anagrafiche/pages/ClienteForm';
import ArticoliList from '@articoli/pages/ArticoliList';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';

function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginForm />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Layout>
                <Dashboard />
              </Layout>
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

        <Route
          path="/articoli"
          element={
            <PrivateRoute>
              <Layout>
                <ArticoliList />
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

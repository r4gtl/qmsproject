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
import ArticoloForm from '@articoli/pages/ArticoloForm';
import ProceduraPage from '@articoli/pages/ProceduraPage';
import NewProceduraPage from '@articoli/pages/NewProceduraPage';
import TabelleGenerichePage from '@articoli/pages/TabelleGenerichePage';
import ElencoTestForm from '@articoli/components/TabelleGeneriche/ElencoTestForm';
import FaseLavoroForm from '@articoli/components/TabelleGeneriche/FaseLavoroForm';
import CodiceLavorazioneForm from '@articoli/components/TabelleGeneriche/CodiceLavorazioneForm';
// Human Resources
import EmployeesPage from './apps/human-resources/pages/EmployeesPage';
import EmployeeForm from './apps/human-resources/pages/EmployeeForm';
import TabelleGenericheHRPage from './apps/human-resources/pages/TabelleGenericheHRPage';
import RegistroOreLavoroListPage from './apps/human-resources/pages/RegistroOreLavoroListPage';
import RegistroOreLavoroFormPage from './apps/human-resources/pages/RegistroOreLavoroFormPage';
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
        <Route
          path="/articoli/new"
          element={
            <PrivateRoute>
              <Layout>
                <ArticoloForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/:articoloId/procedure/new"
          element={
            <PrivateRoute>
              <Layout>
                <NewProceduraPage />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/:articoloId/procedure/:proceduraId"
          element={
            <PrivateRoute>
              <Layout>
                <ProceduraPage />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/:id"
          element={
            <PrivateRoute>
              <Layout>
                <ArticoloForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/elenco-test/new"
          element={
            <PrivateRoute>
              <Layout>
                <ElencoTestForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/elenco-test/:id"
          element={
            <PrivateRoute>
              <Layout>
                <ElencoTestForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/fasi-lavoro/new"
          element={
            <PrivateRoute>
              <Layout>
                <FaseLavoroForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/fasi-lavoro/:id"
          element={
            <PrivateRoute>
              <Layout>
                <FaseLavoroForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/codici-lavorazione/new"
          element={
            <PrivateRoute>
              <Layout>
                <CodiceLavorazioneForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle/codici-lavorazione/:id"
          element={
            <PrivateRoute>
              <Layout>
                <CodiceLavorazioneForm />
              </Layout>
            </PrivateRoute>
          }
        />

        <Route
          path="/articoli/tabelle"
          element={
            <PrivateRoute>
              <Layout>
                <TabelleGenerichePage />
              </Layout>
            </PrivateRoute>
          }
        />

        {/* Human Resources */}
        <Route
          path="/human-resources"
          element={<Navigate to="/human-resources/dipendenti" replace />}
        />
        <Route
          path="/human-resources/dipendenti"
          element={
            <PrivateRoute>
              <Layout>
                <EmployeesPage />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/dipendenti/new"
          element={
            <PrivateRoute>
              <Layout>
                <EmployeeForm />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/dipendenti/:id"
          element={
            <PrivateRoute>
              <Layout>
                <EmployeeForm />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/tabelle"
          element={
            <PrivateRoute>
              <Layout>
                <TabelleGenericheHRPage />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/registro-ore-lavoro"
          element={
            <PrivateRoute>
              <Layout>
                <RegistroOreLavoroListPage />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/registro-ore-lavoro/new"
          element={
            <PrivateRoute>
              <Layout>
                <RegistroOreLavoroFormPage />
              </Layout>
            </PrivateRoute>
          }
        />
        <Route
          path="/human-resources/registro-ore-lavoro/:id"
          element={
            <PrivateRoute>
              <Layout>
                <RegistroOreLavoroFormPage />
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

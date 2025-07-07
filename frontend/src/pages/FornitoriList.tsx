import React, { useEffect, useState } from 'react';
import { Button, Form, Table, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';
import Layout from '@/components/Layout/Layout';

interface Fornitore {
  id: number;
  ragionesociale: string;
  country: string;
  categoria: string;
}

const PAGE_SIZE = 50;

export default function FornitoriList() {
  const navigate = useNavigate();
  const [fornitori, setFornitori] = useState<Fornitore[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    ragionesociale: '',
    country: '',
    categoria: '',
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchFornitori = async () => {
    setLoading(true);
    try {
      console.log('PARAMS chiamata:', {
        page,
        ...filters,
      });

      const response = await axios.get('http://localhost:8000/api/fornitori/', {
        params: {
          page,
          ...filters,
        },
      });
      console.log('RISPOSTA:', response.data);
      setFornitori(response.data.results);
      setTotalPages(Math.ceil(response.data.count / PAGE_SIZE));
    } catch (err) {
      console.error('Errore nella chiamata:', err);
      toast.error('Errore nel caricamento fornitori');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFornitori();
  }, [page, filters]);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Sicuro di voler eliminare?')) return;
    try {
      await axios.delete(`/api/fornitori/${id}/`);
      toast.success('Fornitore eliminato');
      fetchFornitori(); // ricarica dati
    } catch {
      toast.error('Errore durante eliminazione');
    }
  };

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPage(1); // reset alla prima pagina
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Layout>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Fornitori</h2>
        <Button onClick={() => navigate('/fornitori/nuovo')}>Aggiungi</Button>
      </div>

      <div className="mb-2">
        <Form.Label className="fw-bold">Filtri</Form.Label>
      </div>
      <Form className="mb-3 row g-2">
        <Form.Group className="col-md-3">
          <Form.Control
            name="ragionesociale"
            value={filters.ragionesociale}
            onChange={handleFilterChange}
            placeholder="Ragione Sociale"
          />
        </Form.Group>
        <Form.Group className="col-md-3">
          <Form.Control
            name="country"
            value={filters.country}
            onChange={handleFilterChange}
            placeholder="Paese"
          />
        </Form.Group>
        <Form.Group className="col-md-3">
          <Form.Control
            name="categoria"
            value={filters.categoria}
            onChange={handleFilterChange}
            placeholder="Categoria"
          />
        </Form.Group>
        <div className="col-md-3">
          <Button
            variant="outline-secondary"
            onClick={() => {
              setFilters({ ragionesociale: '', country: '', categoria: '' });
              setPage(1);
            }}
          >
            Reset filtri
          </Button>
        </div>
      </Form>

      {loading ? (
        <div className="text-center my-5">
          <Spinner animation="border" />
        </div>
      ) : (
        <>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Ragione Sociale</th>
                <th>Paese</th>
                <th>Categoria</th>
                <th>Azioni</th>
              </tr>
            </thead>
            <tbody>
              {Array.isArray(fornitori) && fornitori.length > 0 ? (
                fornitori.map((f) => (
                  <tr key={f.id}>
                    <td>{f.ragionesociale}</td>
                    <td>{f.country}</td>
                    <td>{f.categoria}</td>
                    <td>
                      <Button
                        size="sm"
                        variant="outline-primary"
                        onClick={() => navigate(`/fornitori/${f.id}/modifica`)}
                        className="me-2"
                      >
                        Modifica
                      </Button>
                      <Button
                        size="sm"
                        variant="outline-danger"
                        onClick={() => handleDelete(f.id)}
                      >
                        Elimina
                      </Button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="text-center">
                    Nessun fornitore trovato.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>

          <div className="d-flex justify-content-between align-items-center mt-3">
            <Button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              &lt; Precedente
            </Button>
            <span>
              Pagina {page} di {totalPages}
            </span>
            <Button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
            >
              Successiva &gt;
            </Button>
          </div>
        </>
      )}
    </Layout>
  );
}

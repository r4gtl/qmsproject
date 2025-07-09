import { useEffect, useState } from 'react';
import {
  Button,
  Container,
  Form,
  Table,
  Pagination,
  Spinner,
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from '@/api/axios';
import CategoriaModal from '../components/CategoriaModal';
import Layout from '../components/Layout/Layout';
import { toast } from 'react-toastify';
import type { Fornitore } from '@/types/anagrafiche';

const PAGE_SIZE = 50;

export default function FornitoriList() {
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [filters, setFilters] = useState({
    ragionesociale: '',
    country: '',
    categoria: '',
  });
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showModal, setShowModal] = useState(false);

  const navigate = useNavigate();

  const fetchFornitori = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/anagrafiche/fornitori/', {
        params: {
          page: currentPage,
          ...filters,
        },
      });
      setFornitori(response.data.results);
      setTotalPages(Math.ceil(response.data.count / PAGE_SIZE));
    } catch (error) {
      toast.error('Errore nel caricamento fornitori');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFornitori();
  }, [currentPage, filters]);

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
    setCurrentPage(1);
  };

  const handleCategoriaSelect = (categoria: string) => {
    setShowModal(false);
    navigate(`/fornitori/nuovo/${categoria}`);
  };

  const handlePageChange = (pageNumber: number) => {
    setCurrentPage(pageNumber);
  };

  const handleDelete = async (id: number) => {
    const conferma = window.confirm(
      'Sei sicuro di voler eliminare questo fornitore?'
    );
    if (!conferma) return;
    try {
      await axios.delete(`/anagrafiche/fornitori/${id}/`);
      toast.success('Fornitore eliminato con successo');
      fetchFornitori();
    } catch (error) {
      toast.error("Errore durante l'eliminazione");
    }
  };

  return (
    <Layout>
      <Container>
        <div className="d-flex justify-content-between align-items-center my-3">
          <h3>Fornitori</h3>
          <Button variant="primary" onClick={() => setShowModal(true)}>
            Aggiungi
          </Button>
        </div>

        <CategoriaModal
          show={showModal}
          onHide={() => setShowModal(false)}
          onSelect={handleCategoriaSelect}
        />

        <Table striped bordered hover>
          <thead>
            <tr>
              <th>
                Ragione Sociale
                <Form.Control
                  size="sm"
                  type="text"
                  placeholder="Filtro..."
                  name="ragionesociale"
                  value={filters.ragionesociale}
                  onChange={handleFilterChange}
                />
              </th>
              <th>
                Paese
                <Form.Control
                  size="sm"
                  type="text"
                  placeholder="Filtro..."
                  name="country"
                  value={filters.country}
                  onChange={handleFilterChange}
                />
              </th>
              <th>
                Categoria
                <Form.Control
                  size="sm"
                  type="text"
                  placeholder="Filtro..."
                  name="categoria"
                  value={filters.categoria}
                  onChange={handleFilterChange}
                />
              </th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={4} className="text-center">
                  <Spinner animation="border" size="sm" /> Caricamento...
                </td>
              </tr>
            ) : fornitori.length > 0 ? (
              fornitori.map((f) => (
                <tr key={f.id}>
                  <td
                    onClick={() => navigate(`/fornitori/${f.id}/modifica`)}
                    style={{ cursor: 'pointer' }}
                  >
                    {f.ragionesociale}
                  </td>
                  <td>{f.country}</td>
                  <td>{f.categoria}</td>
                  <td>
                    <Button
                      variant="outline-danger"
                      size="sm"
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

        <Pagination>
          {Array.from({ length: totalPages }, (_, i) => (
            <Pagination.Item
              key={i + 1}
              active={i + 1 === currentPage}
              onClick={() => handlePageChange(i + 1)}
            >
              {i + 1}
            </Pagination.Item>
          ))}
        </Pagination>
      </Container>
    </Layout>
  );
}

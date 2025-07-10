import { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Form,
  InputGroup,
  Pagination,
  Spinner,
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import type { Cliente } from '@/apps/anagrafiche/types/anagrafiche';
import instance from '@/api/axios';
import { toast } from 'react-toastify';

/* resta da generare ClienteForm */

const ClientiList = () => {
  const [clienti, setClienti] = useState<Cliente[]>([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const fetchClienti = async () => {
    setLoading(true);
    try {
      const response = await instance.get(`/anagrafiche/clienti/`, {
        params: {
          search,
          ordering: 'ragionesociale',
          page,
        },
      });
      setClienti(response.data.results);
      setCount(Math.ceil(response.data.count / 50));
    } catch (error) {
      console.error('Errore nel recupero dei clienti', error);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchClienti();
  }, [search, page]);

  const handleDelete = async (id: number) => {
    const conferma = window.confirm(
      'Sei sicuro di voler eliminare questo cliente?'
    );
    if (!conferma) return;
    try {
      await instance.delete(`/anagrafiche/clienti/${id}/`);
      toast.success('Cliente eliminato con successo');
      fetchClienti();
    } catch (error) {
      toast.error("Errore durante l'eliminazione");
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between mb-3">
        <h2>Clienti</h2>
        <Button onClick={() => navigate('/clienti/nuovo')}>Aggiungi</Button>
      </div>

      <InputGroup className="mb-3">
        <Form.Control
          placeholder="Cerca per ragione sociale..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
        />
      </InputGroup>

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Ragione Sociale</th>
            <th>Indirizzo</th>
            <th>Telefono</th>
            <th>Email</th>
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
          ) : clienti.length > 0 ? (
            clienti.map((cliente) => (
              <tr
                key={cliente.id}
                onClick={() => navigate(`/clienti/${cliente.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <td>{cliente.ragionesociale}</td>
                <td>{cliente.indirizzo}</td>
                <td>{cliente.telefono}</td>
                <td>{cliente.email}</td>
                <td onClick={(e) => e.stopPropagation()}>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(cliente.id)}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={4} className="text-center">
                Nessun cliente trovato.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Pagination>
        {[...Array(count)].map((_, i) => (
          <Pagination.Item
            key={i + 1}
            active={i + 1 === page}
            onClick={() => setPage(i + 1)}
          >
            {i + 1}
          </Pagination.Item>
        ))}
      </Pagination>
    </div>
  );
};

export default ClientiList;

import { useEffect, useState } from 'react';
import { Table, Button, Form, InputGroup, Pagination } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import type { Cliente } from '@/types/anagrafiche';

/* resta da generare ClienteForm */

const ClientiList = () => {
  const [clienti, setClienti] = useState<Cliente[]>([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const navigate = useNavigate();

  const fetchClienti = async () => {
    try {
      const response = await axios.get(`/api/clienti/`, {
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
    }
  };
  useEffect(() => {
    fetchClienti();
  }, [search, page]);

  const handleDelete = async (id: number) => {
    if (window.confirm('Sei sicuro di voler eliminare questo cliente?')) {
      await axios.delete(`api/clienti/${id}/`);
      fetchClienti();
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between mb-3">
        <h2>Clienti</h2>
        <Button onClick={() => navigate('/clienti/nuovo')}>
          Nuovo Cliente
        </Button>
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
          {clienti.map((cliente) => (
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
          ))}
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

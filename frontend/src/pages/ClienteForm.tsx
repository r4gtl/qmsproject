import { FormEvent, useEffect, useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import type { Cliente } from '@/types/anagrafiche';

const ClienteForm = () => {
  const [cliente, setCliente] = useState<Cliente>({
    ragionesociale: '',
    indirizzo: '',
    telefono: '',
    email: '',
    partita_iva: '',
  });

  const navigate = useNavigate();
  const { id } = useParams();

  const isEdit = !!id;

  useEffect(() => {
    if (isEdit) {
      axios.get(`/api/clienti/${id}/`).then((res) => setCliente(res.data));
    }
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await axios.put(`/api/clienti/${id}/`, cliente);
    } else {
      await axios.post(`/api/clienti/`, cliente);
    }
    navigate('/clienti');
  };

  return (
    <div className="container mt-4">
      <h2>{isEdit ? 'Modifica Cliente' : 'Nuovo Cliente'}</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Ragione Sociale</Form.Label>
          <Form.Control
            required
            value={cliente.ragionesociale}
            onChange={(e) =>
              setCliente({ ...cliente, ragionesociale: e.target.value })
            }
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Indirizzo</Form.Label>
          <Form.Control
            value={cliente.indirizzo}
            onChange={(e) =>
              setCliente({ ...cliente, indirizzo: e.target.value })
            }
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Telefono</Form.Label>
          <Form.Control
            value={cliente.telefono}
            onChange={(e) =>
              setCliente({ ...cliente, telefono: e.target.value })
            }
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            value={cliente.email}
            onChange={(e) => setCliente({ ...cliente, email: e.target.value })}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Partita IVA</Form.Label>
          <Form.Control
            value={cliente.partita_iva}
            onChange={(e) =>
              setCliente({ ...cliente, partita_iva: e.target.value })
            }
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          {isEdit ? 'Salva modifiche' : 'Crea cliente'}
        </Button>
      </Form>
    </div>
  );
};

export default ClienteForm;

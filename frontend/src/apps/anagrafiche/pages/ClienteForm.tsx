import { FormEvent, useEffect, useState, useMemo } from 'react';
import { Button, Form } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import type { Cliente } from '@/apps/anagrafiche/types/anagrafiche';
import instance from '@/api/axios';

import { toast } from 'react-toastify';

import Select from 'react-select';
import countryList from 'react-select-country-list';

const ClienteForm = () => {
  const [cliente, setCliente] = useState<Cliente>({
    ragionesociale: '',
    indirizzo: '',
    telefono: '',
    email: '',
    partita_iva: '',
    country: '',
  });

  const navigate = useNavigate();
  const { id } = useParams();
  const countryOptions = useMemo(() => countryList().getData(), []);
  const isEdit = !!id;

  useEffect(() => {
    if (isEdit) {
      instance
        .get(`/anagrafiche/clienti/${id}/`)
        .then((res) => setCliente(res.data));
    }
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      await instance.put(`/anagrafiche/clienti/${id}/`, cliente);
    } else {
      await instance.post(`/anagrafiche/clienti/`, cliente);
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

        <Form.Group className="mb-3">
          <Form.Label>Paese</Form.Label>
          <Select
            options={countryOptions}
            value={countryOptions.find((opt) => opt.value === cliente.country)}
            onChange={(val) =>
              setCliente((prev) => ({
                ...prev,
                country: val?.value || '',
              }))
            }
          />
        </Form.Group>
        <Button
          variant="secondary"
          onClick={() => navigate('/clienti')}
          className="me-2"
        >
          Annulla
        </Button>

        <Button variant="primary" type="submit">
          {isEdit ? 'Salva modifiche' : 'Crea cliente'}
        </Button>
      </Form>
    </div>
  );
};

export default ClienteForm;

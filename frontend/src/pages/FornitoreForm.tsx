import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card } from 'react-bootstrap';
import axios from '@/api/axios';
import { toast } from 'react-toastify';

interface FornitoreFormProps {
  mode: 'create' | 'edit';
}

export default function FornitoreForm({ mode }: FornitoreFormProps) {
  const navigate = useNavigate();
  const { id, categoria } = useParams();

  const [formData, setFormData] = useState({
    ragionesociale: '',
    country: '',
    categoria: categoria || '',
    e_mail: '',
    indirizzo: '',
    cap: '',
    city: '',
    provincia: '',
  });

  useEffect(() => {
    if (mode === 'edit' && id) {
      axios
        .get(`/anagrafiche/fornitori/${id}/`)
        .then((res) => setFormData(res.data))
        .catch(() => toast.error('Errore nel caricamento fornitore'));
    }
  }, [mode, id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const apiCall =
      mode === 'edit'
        ? axios.put(`/anagrafiche/fornitori/${id}/`, formData)
        : axios.post(`/anagrafiche/fornitori/`, formData);

    apiCall
      .then(() => {
        toast.success('Fornitore salvato con successo');
        navigate('/fornitori');
      })
      .catch(() => {
        toast.error('Errore durante il salvataggio');
      });
  };

  return (
    <Card className="p-4">
      <h4>{mode === 'edit' ? 'Modifica' : 'Nuovo'} Fornitore</h4>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Ragione Sociale</Form.Label>
          <Form.Control
            type="text"
            name="ragionesociale"
            value={formData.ragionesociale}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            name="e_mail"
            value={formData.e_mail}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Paese</Form.Label>
          <Form.Control
            type="text"
            name="country"
            value={formData.country}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Categoria</Form.Label>
          <Form.Control
            type="text"
            name="categoria"
            value={formData.categoria}
            readOnly={mode === 'create'} // imposta da URL
          />
        </Form.Group>

        {/* altri campi comuni o dinamici qui */}

        <div className="d-flex justify-content-end mt-4">
          <Button type="submit" variant="primary">
            Salva
          </Button>
        </div>
      </Form>
    </Card>
  );
}

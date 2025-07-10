import { useEffect, useState, useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card } from 'react-bootstrap';
import axios from '@/api/axios';
import { toast } from 'react-toastify';

import Select from 'react-select';
import countryList from 'react-select-country-list';

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

    // Campi per PELLI
    is_lwg: false,
    urn: '',
    tipo_fornitore: '',
    latitude: '',
    longitude: '',

    // Campi per PRODOTTI CHIMICI
    id_zdhc: '',

    // Campi per LAVORAZIONI ESTERNE
    audit: '',

    // Campi per MANUTENZIONI
    manutenzione_note: '',
  });

  const countryOptions = useMemo(() => countryList().getData(), []);

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
    const cleanData = { ...formData };

    // Pulisci i campi opzionali numerici
    if (cleanData.latitude === '') cleanData.latitude = null;
    if (cleanData.longitude === '') cleanData.longitude = null;

    const apiCall =
      mode === 'edit'
        ? axios.put(`/anagrafiche/fornitori/${id}/`, cleanData)
        : axios.post(`/anagrafiche/fornitori/`, cleanData);

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
          <Select
            options={countryOptions}
            value={countryOptions.find((opt) => opt.value === formData.country)}
            onChange={(val) =>
              setFormData((prev) => ({
                ...prev,
                country: val?.value || '',
              }))
            }
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Categoria</Form.Label>
          <Form.Control
            type="text"
            name="categoria"
            value={formData.categoria}
            onChange={handleChange}
            readOnly={mode === 'create'} // imposta da URL
          />
        </Form.Group>

        {/* Campi dinamici */}

        {formData.categoria === 'pelli' && (
          <>
            <Form.Group className="mb-3" controlId="is_lwg">
              <Form.Check
                type="checkbox"
                label="LWG"
                checked={formData.is_lwg}
                onChange={(e) =>
                  setFormData({ ...formData, is_lwg: e.target.checked })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="urn">
              <Form.Label>URN</Form.Label>
              <Form.Control
                type="text"
                value={formData.urn || ''}
                onChange={(e) =>
                  setFormData({ ...formData, urn: e.target.value })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="tipo_fornitore">
              <Form.Label>Tipo Fornitore</Form.Label>
              <Form.Select
                value={formData.tipo_fornitore || ''}
                onChange={(e) =>
                  setFormData({ ...formData, tipo_fornitore: e.target.value })
                }
              >
                <option value="">-- Seleziona --</option>
                <option value="macello">Macello</option>
                <option value="commerciante">Commerciante</option>
                <option value="altro">Altro</option>
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="latitude">
              <Form.Label>Latitudine</Form.Label>
              <Form.Control
                type="number"
                step="any"
                value={formData.latitude || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    latitude: parseFloat(e.target.value),
                  })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="longitude">
              <Form.Label>Longitudine</Form.Label>
              <Form.Control
                type="number"
                step="any"
                value={formData.longitude || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    longitude: parseFloat(e.target.value),
                  })
                }
              />
            </Form.Group>
            {formData.latitude && formData.longitude && (
              <Button
                variant="outline-primary"
                size="sm"
                target="_blank"
                href={`https://www.google.com/maps?q=${formData.latitude},${formData.longitude}`}
              >
                Apri in Google Maps
              </Button>
            )}
          </>
        )}

        {formData.categoria === 'prodotti chimici' && (
          <Form.Group className="mb-3" controlId="id_zdhc">
            <Form.Label>ID ZDHC</Form.Label>
            <Form.Control
              type="text"
              value={formData.id_zdhc || ''}
              onChange={(e) =>
                setFormData({ ...formData, id_zdhc: e.target.value })
              }
            />
          </Form.Group>
        )}

        {formData.categoria === 'lavorazioni esterne' && (
          <Form.Group className="mb-3" controlId="audit">
            <Form.Label>Audit</Form.Label>
            <Form.Select
              value={formData.audit || ''}
              onChange={(e) =>
                setFormData({ ...formData, audit: e.target.value })
              }
            >
              <option value="">-- Seleziona --</option>
              <option value="not_audited">Nessun Audit</option>
              <option value="leather_manufacturer_audit_protocol">
                Leather Manufacturer Audit Protocol
              </option>
              <option value="subcontractor_audit_protocol">
                Subcontractor Audit Protocol
              </option>
              <option value="mini_audit_protocol">Mini-Audit Protocol</option>
            </Form.Select>
          </Form.Group>
        )}

        {formData.categoria === 'manutenzioni' && (
          <Form.Group className="mb-3" controlId="manutenzione_note">
            <Form.Label>Note Manutenzione</Form.Label>
            <Form.Control
              type="text"
              value={formData.manutenzione_note || ''}
              onChange={(e) =>
                setFormData({ ...formData, manutenzione_note: e.target.value })
              }
            />
          </Form.Group>
        )}

        {/* altri campi comuni o dinamici qui */}

        <div className="d-flex justify-content-end mt-4">
          <Button
            variant="secondary"
            onClick={() => navigate('/fornitori')}
            className="me-2"
          >
            Annulla
          </Button>

          <Button type="submit" variant="primary">
            Salva
          </Button>
        </div>
      </Form>
    </Card>
  );
}

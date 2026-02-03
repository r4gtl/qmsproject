/**
 * RegistroOreLavoroFormPage - Form per creare/modificare registro ore lavoro
 *
 * Features:
 * - Campi principali: entry_year, entry_month, ore_lavorabili, ore_lavorate
 * - Campi secondari (tutti i restanti)
 * - Modalità create/edit basata su :id param
 * - Pulsanti Salva / Annulla
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  Form,
  Button,
  Spinner,
  Row,
  Col,
  Alert,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaClock, FaSave, FaTimes } from 'react-icons/fa';
import {
  getRegistroOreLavoro,
  createRegistroOreLavoro,
  updateRegistroOreLavoro,
} from '../api';
import type { RegistroOreLavoroDetail, RegistroOreLavoroCreate } from '../types';
import { MONTH_CHOICES } from '../types';

// Generate year options
const currentYear = new Date().getFullYear();
const YEAR_OPTIONS = Array.from({ length: currentYear - 2000 + 2 }, (_, i) => currentYear + 1 - i);

interface FormData {
  entry_year: number;
  entry_month: number;
  ore_lavorabili: string;
  ore_lavorate: string;
  straordinari: string;
  ferie_permessi: string;
  permessi_speciali: string;
  maternità: string;
  infortunio: string;
  formazione: string;
  formazione_neoassunti: string;
  malattia: string;
  n_infortuni: string;
  n_infortuni_itinere: string;
  n_malattie_professionali: string;
  ore_malattie_professionali: string;
  permessi_non_retribuiti: string;
  assenze_ingiustificate: string;
  note: string;
}

const initialFormData: FormData = {
  entry_year: currentYear,
  entry_month: new Date().getMonth() + 1,
  ore_lavorabili: '',
  ore_lavorate: '',
  straordinari: '',
  ferie_permessi: '',
  permessi_speciali: '',
  maternità: '',
  infortunio: '',
  formazione: '',
  formazione_neoassunti: '',
  malattia: '',
  n_infortuni: '',
  n_infortuni_itinere: '',
  n_malattie_professionali: '',
  ore_malattie_professionali: '',
  permessi_non_retribuiti: '',
  assenze_ingiustificate: '',
  note: '',
};

export default function RegistroOreLavoroFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id && id !== 'new';

  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load existing record if editing
  useEffect(() => {
    if (isEdit) {
      loadRecord();
    }
  }, [id, isEdit]);

  const loadRecord = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getRegistroOreLavoro(Number(id));
      const data: RegistroOreLavoroDetail = res.data;
      setFormData({
        entry_year: data.entry_year,
        entry_month: data.entry_month,
        ore_lavorabili: data.ore_lavorabili?.toString() ?? '',
        ore_lavorate: data.ore_lavorate?.toString() ?? '',
        straordinari: data.straordinari?.toString() ?? '',
        ferie_permessi: data.ferie_permessi?.toString() ?? '',
        permessi_speciali: data.permessi_speciali?.toString() ?? '',
        maternità: data.maternità?.toString() ?? '',
        infortunio: data.infortunio?.toString() ?? '',
        formazione: data.formazione?.toString() ?? '',
        formazione_neoassunti: data.formazione_neoassunti?.toString() ?? '',
        malattia: data.malattia?.toString() ?? '',
        n_infortuni: data.n_infortuni?.toString() ?? '',
        n_infortuni_itinere: data.n_infortuni_itinere?.toString() ?? '',
        n_malattie_professionali: data.n_malattie_professionali?.toString() ?? '',
        ore_malattie_professionali: data.ore_malattie_professionali?.toString() ?? '',
        permessi_non_retribuiti: data.permessi_non_retribuiti?.toString() ?? '',
        assenze_ingiustificate: data.assenze_ingiustificate?.toString() ?? '',
        note: data.note ?? '',
      });
    } catch (err: any) {
      setError('Errore nel caricamento del registro.');
      toast.error('Errore caricamento dati');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof FormData, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const parseIntOrNull = (val: string): number | null => {
    if (!val || val.trim() === '') return null;
    const parsed = parseInt(val, 10);
    return isNaN(parsed) ? null : parsed;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.entry_year) {
      toast.warning("L'anno è obbligatorio");
      return;
    }
    if (!formData.entry_month) {
      toast.warning('Il mese è obbligatorio');
      return;
    }

    try {
      setSaving(true);
      const payload: RegistroOreLavoroCreate = {
        entry_year: formData.entry_year,
        entry_month: formData.entry_month,
        ore_lavorabili: parseIntOrNull(formData.ore_lavorabili),
        ore_lavorate: parseIntOrNull(formData.ore_lavorate),
        straordinari: parseIntOrNull(formData.straordinari),
        ferie_permessi: parseIntOrNull(formData.ferie_permessi),
        permessi_speciali: parseIntOrNull(formData.permessi_speciali),
        maternità: parseIntOrNull(formData.maternità),
        infortunio: parseIntOrNull(formData.infortunio),
        formazione: parseIntOrNull(formData.formazione),
        formazione_neoassunti: parseIntOrNull(formData.formazione_neoassunti),
        malattia: parseIntOrNull(formData.malattia),
        n_infortuni: parseIntOrNull(formData.n_infortuni),
        n_infortuni_itinere: parseIntOrNull(formData.n_infortuni_itinere),
        n_malattie_professionali: parseIntOrNull(formData.n_malattie_professionali),
        ore_malattie_professionali: parseIntOrNull(formData.ore_malattie_professionali),
        permessi_non_retribuiti: parseIntOrNull(formData.permessi_non_retribuiti),
        assenze_ingiustificate: parseIntOrNull(formData.assenze_ingiustificate),
        note: formData.note.trim() || null,
      };

      if (isEdit) {
        await updateRegistroOreLavoro(Number(id), payload);
        toast.success('Registro aggiornato');
      } else {
        await createRegistroOreLavoro(payload);
        toast.success('Registro creato');
      }
      navigate('/human-resources/registro-ore-lavoro');
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore durante il salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate('/human-resources/registro-ore-lavoro');
  };

  if (loading) {
    return (
      <Container className="my-4 text-center">
        <Spinner animation="border" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="my-4">
        <Alert variant="danger">{error}</Alert>
        <Button variant="secondary" onClick={handleCancel}>
          Torna alla lista
        </Button>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Card className="shadow-sm">
        <Card.Header className="d-flex align-items-center">
          <FaClock className="me-2" />
          <span className="fw-bold">
            {isEdit ? 'Modifica Registro Ore Lavoro' : 'Nuovo Registro Ore Lavoro'}
          </span>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            {/* Periodo */}
            <h6 className="text-muted mb-3">Periodo</h6>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>
                    Anno <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formData.entry_year}
                    onChange={(e) => handleChange('entry_year', Number(e.target.value))}
                    required
                  >
                    {YEAR_OPTIONS.map((y) => (
                      <option key={y} value={y}>
                        {y}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>
                    Mese <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formData.entry_month}
                    onChange={(e) => handleChange('entry_month', Number(e.target.value))}
                    required
                  >
                    {MONTH_CHOICES.map((m) => (
                      <option key={m.value} value={m.value}>
                        {m.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            {/* Ore principali */}
            <h6 className="text-muted mb-3">Ore Principali</h6>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Lavorabili</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.ore_lavorabili}
                    onChange={(e) => handleChange('ore_lavorabili', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Lavorate</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.ore_lavorate}
                    onChange={(e) => handleChange('ore_lavorate', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Straordinari</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.straordinari}
                    onChange={(e) => handleChange('straordinari', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Assenze */}
            <h6 className="text-muted mb-3">Assenze e Permessi</h6>
            <Row className="mb-3">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ferie/Permessi</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.ferie_permessi}
                    onChange={(e) => handleChange('ferie_permessi', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Permessi Speciali</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.permessi_speciali}
                    onChange={(e) => handleChange('permessi_speciali', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Maternità</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.maternità}
                    onChange={(e) => handleChange('maternità', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Malattia</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.malattia}
                    onChange={(e) => handleChange('malattia', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Permessi Non Retribuiti</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.permessi_non_retribuiti}
                    onChange={(e) => handleChange('permessi_non_retribuiti', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Assenze Ingiustificate</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.assenze_ingiustificate}
                    onChange={(e) => handleChange('assenze_ingiustificate', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Infortuni e malattie professionali */}
            <h6 className="text-muted mb-3">Infortuni e Malattie Professionali</h6>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Infortunio</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.infortunio}
                    onChange={(e) => handleChange('infortunio', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>N. Infortuni</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.n_infortuni}
                    onChange={(e) => handleChange('n_infortuni', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>N. Infortuni Itinere</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.n_infortuni_itinere}
                    onChange={(e) => handleChange('n_infortuni_itinere', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>N. Malattie Professionali</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.n_malattie_professionali}
                    onChange={(e) => handleChange('n_malattie_professionali', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Malattie Professionali</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.ore_malattie_professionali}
                    onChange={(e) => handleChange('ore_malattie_professionali', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Formazione */}
            <h6 className="text-muted mb-3">Formazione</h6>
            <Row className="mb-4">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Formazione</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.formazione}
                    onChange={(e) => handleChange('formazione', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore Formazione Neoassunti</Form.Label>
                  <Form.Control
                    type="number"
                    value={formData.formazione_neoassunti}
                    onChange={(e) => handleChange('formazione_neoassunti', e.target.value)}
                    min={0}
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Note */}
            <h6 className="text-muted mb-3">Note</h6>
            <Row className="mb-4">
              <Col md={12}>
                <Form.Group>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={formData.note}
                    onChange={(e) => handleChange('note', e.target.value)}
                    placeholder="Note aggiuntive..."
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Buttons */}
            <div className="d-flex justify-content-end gap-2">
              <Button variant="secondary" onClick={handleCancel} disabled={saving}>
                <FaTimes className="me-1" /> Annulla
              </Button>
              <Button variant="primary" type="submit" disabled={saving}>
                {saving ? (
                  <Spinner animation="border" size="sm" />
                ) : (
                  <>
                    <FaSave className="me-1" /> Salva
                  </>
                )}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}

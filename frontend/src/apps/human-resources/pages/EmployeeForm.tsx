/**
 * EmployeeForm - Form dipendente con Tabs
 *
 * Tab 1: Dati dipendente (create/edit)
 * Tab 2: Valutazioni (solo in edit mode)
 */
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Card,
  Form,
  Button,
  Row,
  Col,
  Tabs,
  Tab,
  Spinner,
  Alert,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getDipendente,
  createDipendente,
  updateDipendente,
  getReparti,
  getMansioni,
} from '../api';
import type {
  HumanResourceDetail,
  HumanResourceCreate,
  Ward,
  Role,
} from '../types';
import {
  GENDER_CHOICES,
  CONTRATTO_CHOICES,
  ORARIO_CHOICES,
} from '../types';
import ValutazioniTab from '../components/ValutazioniTab';

export default function EmployeeForm() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEditMode = !!id && id !== 'new';

  // Form state
  const [formData, setFormData] = useState<HumanResourceCreate>({
    cognomedipendente: '',
    nomedipendente: '',
    data_nascita: null,
    country: null,
    gender: null,
    contratto: null,
    orario: null,
    dataassunzione: '',
    datadimissioni: null,
    fk_mansione: null,
    fk_reparto: null,
    qualifica: null,
    commenti: null,
  });

  // Dipendente caricato (per edit mode)
  const [dipendente, setDipendente] = useState<HumanResourceDetail | null>(null);

  // Lookup data
  const [reparti, setReparti] = useState<Ward[]>([]);
  const [mansioni, setMansioni] = useState<Role[]>([]);

  // UI state
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('dati');

  // Carica lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [repartiRes, mansioniRes] = await Promise.all([
          getReparti({ page_size: 1000 }),
          getMansioni({ page_size: 1000 }),
        ]);
        setReparti(repartiRes.data.results);
        setMansioni(mansioniRes.data.results);
      } catch {
        toast.error('Errore caricamento dati');
      }
    };
    loadLookups();
  }, []);

  // Carica dipendente se edit mode
  useEffect(() => {
    if (!isEditMode) return;

    const loadDipendente = async () => {
      try {
        setLoading(true);
        const res = await getDipendente(Number(id));
        const d = res.data;
        setDipendente(d);
        setFormData({
          cognomedipendente: d.cognomedipendente,
          nomedipendente: d.nomedipendente,
          data_nascita: d.data_nascita,
          country: d.country,
          gender: d.gender,
          contratto: d.contratto,
          orario: d.orario,
          dataassunzione: d.dataassunzione,
          datadimissioni: d.datadimissioni,
          fk_mansione: d.fk_mansione,
          fk_reparto: d.fk_reparto,
          qualifica: d.qualifica,
          commenti: d.commenti,
        });
      } catch {
        toast.error('Errore caricamento dipendente');
        navigate('/human-resources/dipendenti');
      } finally {
        setLoading(false);
      }
    };
    loadDipendente();
  }, [id, isEditMode, navigate]);

  // Handle input change
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === '' ? null : value,
    }));
  };

  // Handle number/FK change
  const handleFKChange = (name: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value ? Number(value) : null,
    }));
  };

  // Handle reparto change - reset mansione if not compatible
  const handleRepartoChange = (value: string) => {
    const newRepartoId = value ? Number(value) : null;

    setFormData((prev) => {
      // If current mansione is not compatible with new reparto, reset it
      if (prev.fk_mansione && newRepartoId) {
        const currentMansione = mansioni.find((m) => m.id === prev.fk_mansione);
        // Reset if mansione has a different reparto (not null and not matching)
        if (currentMansione?.fk_reparto && currentMansione.fk_reparto !== newRepartoId) {
          return {
            ...prev,
            fk_reparto: newRepartoId,
            fk_mansione: null,
          };
        }
      }
      return {
        ...prev,
        fk_reparto: newRepartoId,
      };
    });
  };

  // Filtered mansioni based on selected reparto
  // Shows: mansioni with no reparto (generic) + mansioni matching selected reparto
  const filteredMansioni = formData.fk_reparto
    ? mansioni.filter(
        (m) => m.fk_reparto === null || m.fk_reparto === formData.fk_reparto
      )
    : mansioni;

  // Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validazione base
    if (!formData.cognomedipendente?.trim()) {
      toast.warning('Il cognome è obbligatorio');
      return;
    }
    if (!formData.nomedipendente?.trim()) {
      toast.warning('Il nome è obbligatorio');
      return;
    }
    if (!formData.dataassunzione) {
      toast.warning('La data di assunzione è obbligatoria');
      return;
    }

    try {
      setSaving(true);

      if (isEditMode) {
        const res = await updateDipendente(Number(id), formData);
        setDipendente(res.data);
        toast.success('Dipendente aggiornato');
      } else {
        const res = await createDipendente(formData);
        toast.success('Dipendente creato');
        // Naviga al form edit del nuovo dipendente
        navigate(`/human-resources/dipendenti/${res.data.id}`, { replace: true });
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(detail);
    } finally {
      setSaving(false);
    }
  };

  // Callback per refresh valutazioni (dopo modifica)
  const handleValutazioniChange = async () => {
    if (!isEditMode) return;
    // Ricarica dipendente per aggiornare conteggi se necessario
    try {
      const res = await getDipendente(Number(id));
      setDipendente(res.data);
    } catch {
      // silent fail
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" />
        <p className="mt-2">Caricamento dipendente...</p>
      </div>
    );
  }

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <span>
          <Button
            variant="link"
            className="p-0 me-2"
            onClick={() => navigate('/human-resources/dipendenti')}
          >
            ← Indietro
          </Button>
          <strong>
            {isEditMode ? `${dipendente?.full_name}` : 'Nuovo Dipendente'}
          </strong>
        </span>
      </Card.Header>

      <Card.Body>
        <Tabs
          activeKey={activeTab}
          onSelect={(k) => setActiveTab(k || 'dati')}
          className="mb-4"
        >
          {/* TAB 1: Dati Dipendente */}
          <Tab eventKey="dati" title="Dati Dipendente">
            <Form onSubmit={handleSubmit}>
              <Row>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>
                      Cognome <span className="text-danger">*</span>
                    </Form.Label>
                    <Form.Control
                      name="cognomedipendente"
                      value={formData.cognomedipendente || ''}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>
                      Nome <span className="text-danger">*</span>
                    </Form.Label>
                    <Form.Control
                      name="nomedipendente"
                      value={formData.nomedipendente || ''}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Data di Nascita</Form.Label>
                    <Form.Control
                      type="date"
                      name="data_nascita"
                      value={formData.data_nascita || ''}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Genere</Form.Label>
                    <Form.Select
                      name="gender"
                      value={formData.gender || ''}
                      onChange={handleChange}
                    >
                      <option value="">-- Seleziona --</option>
                      {GENDER_CHOICES.map((c) => (
                        <option key={c.value} value={c.value}>
                          {c.label}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Paese</Form.Label>
                    <Form.Control
                      name="country"
                      value={formData.country || ''}
                      onChange={handleChange}
                      placeholder="es: IT"
                    />
                    <Form.Text className="text-muted">
                      Codice ISO (es: IT, DE, FR)
                    </Form.Text>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Qualifica</Form.Label>
                    <Form.Control
                      name="qualifica"
                      value={formData.qualifica || ''}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Contratto</Form.Label>
                    <Form.Select
                      name="contratto"
                      value={formData.contratto || ''}
                      onChange={handleChange}
                    >
                      <option value="">-- Seleziona --</option>
                      {CONTRATTO_CHOICES.map((c) => (
                        <option key={c.value} value={c.value}>
                          {c.label}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Orario</Form.Label>
                    <Form.Select
                      name="orario"
                      value={formData.orario || ''}
                      onChange={handleChange}
                    >
                      <option value="">-- Seleziona --</option>
                      {ORARIO_CHOICES.map((c) => (
                        <option key={c.value} value={c.value}>
                          {c.label}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>
                      Data Assunzione <span className="text-danger">*</span>
                    </Form.Label>
                    <Form.Control
                      type="date"
                      name="dataassunzione"
                      value={formData.dataassunzione || ''}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Data Dimissioni</Form.Label>
                    <Form.Control
                      type="date"
                      name="datadimissioni"
                      value={formData.datadimissioni || ''}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Reparto</Form.Label>
                    <Form.Select
                      value={formData.fk_reparto || ''}
                      onChange={(e) => handleRepartoChange(e.target.value)}
                    >
                      <option value="">-- Seleziona --</option>
                      {reparti.map((r) => (
                        <option key={r.id} value={r.id}>
                          {r.description}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={4}>
                  <Form.Group className="mb-3">
                    <Form.Label>Mansione</Form.Label>
                    <Form.Select
                      value={formData.fk_mansione || ''}
                      onChange={(e) => handleFKChange('fk_mansione', e.target.value)}
                    >
                      <option value="">-- Seleziona --</option>
                      {filteredMansioni.map((m) => (
                        <option key={m.id} value={m.id}>
                          {m.description}
                          {m.fk_reparto_display ? ` (${m.fk_reparto_display})` : ''}
                        </option>
                      ))}
                    </Form.Select>
                    {formData.fk_reparto && filteredMansioni.length < mansioni.length && (
                      <Form.Text className="text-muted">
                        Filtrate per reparto selezionato
                      </Form.Text>
                    )}
                  </Form.Group>
                </Col>
              </Row>

              <Form.Group className="mb-3">
                <Form.Label>Commenti</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  name="commenti"
                  value={formData.commenti || ''}
                  onChange={handleChange}
                />
              </Form.Group>

              {/* Immagine - TODO: upload non implementato */}
              {isEditMode && dipendente?.immagine && (
                <Form.Group className="mb-3">
                  <Form.Label>Immagine</Form.Label>
                  <div>
                    <img
                      src={dipendente.immagine}
                      alt="Foto dipendente"
                      style={{ maxWidth: '150px', maxHeight: '150px' }}
                      className="rounded"
                    />
                  </div>
                  <Form.Text className="text-muted">
                    TODO: Upload immagine non implementato
                  </Form.Text>
                </Form.Group>
              )}

              <div className="text-end">
                <Button
                  variant="secondary"
                  className="me-2"
                  onClick={() => navigate('/human-resources/dipendenti')}
                >
                  Annulla
                </Button>
                <Button variant="primary" type="submit" disabled={saving}>
                  {saving ? (
                    <Spinner animation="border" size="sm" />
                  ) : isEditMode ? (
                    'Salva Modifiche'
                  ) : (
                    'Crea Dipendente'
                  )}
                </Button>
              </div>
            </Form>
          </Tab>

          {/* TAB 2: Valutazioni */}
          <Tab eventKey="valutazioni" title="Valutazioni">
            {!isEditMode ? (
              <Alert variant="info">
                Salva prima il dipendente per poter gestire le valutazioni.
              </Alert>
            ) : (
              <ValutazioniTab
                dipendenteId={Number(id)}
                onValutazioniChange={handleValutazioniChange}
              />
            )}
          </Tab>
        </Tabs>
      </Card.Body>
    </Card>
  );
}

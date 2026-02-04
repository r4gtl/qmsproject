/**
 * RegistroFormazioneFormPage - Form per creare/modificare registro formazione
 *
 * Features:
 * - Card testata con form: data_formazione, fk_corso, fk_fornitore, ore, note
 * - Tabella dettagli (operatori formati) sotto la testata
 * - Pulsante "Aggiungi operatore" -> DettaglioFormazioneFormPage
 * - Delete dettaglio con modal conferma
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
  Table,
  Badge,
  ButtonGroup,
  Modal,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  FaGraduationCap,
  FaSave,
  FaTimes,
  FaPlus,
  FaEdit,
  FaTrash,
  FaFileAlt,
} from 'react-icons/fa';
import {
  getRegistroFormazione,
  createRegistroFormazione,
  updateRegistroFormazione,
  getCorsiFormazione,
  getFornitoriForSelect,
  deleteDettaglioFormazione,
} from '../api/formazioneApi';
import type {
  RegistroFormazioneDetail,
  RegistroFormazioneCreate,
  CorsoFormazione,
  Fornitore,
  DettaglioRegistroFormazione,
} from '../types';
import { extractErrorMessage, parseOreOrNull } from '../utils/drfErrors';

interface FormData {
  data_formazione: string;
  fk_corso: string;
  fk_fornitore: string;
  ore: string;
  note: string;
}

const initialFormData: FormData = {
  data_formazione: new Date().toISOString().split('T')[0],
  fk_corso: '',
  fk_fornitore: '',
  ore: '',
  note: '',
};

export default function RegistroFormazioneFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id && id !== 'new';

  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [dettagli, setDettagli] = useState<DettaglioRegistroFormazione[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Lookups
  const [corsi, setCorsi] = useState<CorsoFormazione[]>([]);
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [loadingLookups, setLoadingLookups] = useState(true);

  // Delete dettaglio modal
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletingDettaglioId, setDeletingDettaglioId] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        setLoadingLookups(true);
        const [corsiRes, fornitoriRes] = await Promise.all([
          getCorsiFormazione({ page_size: 1000 }),
          getFornitoriForSelect(),
        ]);
        setCorsi(corsiRes.data.results);
        setFornitori(fornitoriRes.data.results);
      } catch {
        toast.error('Errore nel caricamento dei dati di lookup');
      } finally {
        setLoadingLookups(false);
      }
    };
    loadLookups();
  }, []);

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
      const res = await getRegistroFormazione(Number(id));
      const data: RegistroFormazioneDetail = res.data;
      setFormData({
        data_formazione: data.data_formazione,
        fk_corso: data.fk_corso?.toString() ?? '',
        fk_fornitore: data.fk_fornitore?.toString() ?? '',
        ore: data.ore?.toString() ?? '',
        note: data.note ?? '',
      });
      setDettagli(data.dettagli || []);
    } catch (err: any) {
      setError('Errore nel caricamento del registro.');
      toast.error('Errore caricamento dati');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.data_formazione) {
      toast.warning('La data formazione è obbligatoria');
      return;
    }
    if (!formData.fk_corso) {
      toast.warning('Il corso è obbligatorio');
      return;
    }

    try {
      setSaving(true);
      const payload: RegistroFormazioneCreate = {
        data_formazione: formData.data_formazione,
        fk_corso: parseInt(formData.fk_corso, 10),
        fk_fornitore: formData.fk_fornitore ? parseInt(formData.fk_fornitore, 10) : null,
        ore: parseOreOrNull(formData.ore),
        note: formData.note.trim() || null,
      };

      if (isEdit) {
        await updateRegistroFormazione(Number(id), payload);
        toast.success('Registro formazione aggiornato');
        loadRecord(); // Reload to get fresh dettagli
      } else {
        const res = await createRegistroFormazione(payload);
        toast.success('Registro formazione creato');
        // Redirect to edit page with new ID
        navigate(`/human-resources/formazione/registri/${res.data.id}`, { replace: true });
      }
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore durante il salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate('/human-resources/formazione');
  };

  // Dettagli handlers
  const handleAddDettaglio = () => {
    navigate(`/human-resources/formazione/registri/${id}/dettagli/new`);
  };

  const handleEditDettaglio = (dettaglioId: number) => {
    navigate(`/human-resources/formazione/registri/${id}/dettagli/${dettaglioId}`);
  };

  const handleDeleteDettaglioClick = (e: React.MouseEvent, dettaglioId: number) => {
    e.stopPropagation();
    setDeletingDettaglioId(dettaglioId);
    setShowDeleteModal(true);
  };

  const handleDeleteDettaglioConfirm = async () => {
    if (!deletingDettaglioId) return;

    try {
      setDeleteLoading(true);
      await deleteDettaglioFormazione(deletingDettaglioId);
      toast.success('Operatore rimosso');
      setShowDeleteModal(false);
      setDeletingDettaglioId(null);
      loadRecord(); // Reload dettagli
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore durante l\'eliminazione'));
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleDeleteDettaglioCancel = () => {
    setShowDeleteModal(false);
    setDeletingDettaglioId(null);
  };

  // Format date
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  if (loading || loadingLookups) {
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
      {/* Testata Form */}
      <Card className="shadow-sm mb-4">
        <Card.Header className="d-flex align-items-center">
          <FaGraduationCap className="me-2" />
          <span className="fw-bold">
            {isEdit ? 'Modifica Registro Formazione' : 'Nuovo Registro Formazione'}
          </span>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row className="mb-3">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>
                    Data Formazione <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.data_formazione}
                    onChange={(e) => handleChange('data_formazione', e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>
                    Corso <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formData.fk_corso}
                    onChange={(e) => handleChange('fk_corso', e.target.value)}
                    required
                  >
                    <option value="">-- Seleziona corso --</option>
                    {corsi.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.descrizione}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Fornitore</Form.Label>
                  <Form.Select
                    value={formData.fk_fornitore}
                    onChange={(e) => handleChange('fk_fornitore', e.target.value)}
                  >
                    <option value="">-- Nessun fornitore --</option>
                    {fornitori.map((f) => (
                      <option key={f.id} value={f.id}>
                        {f.ragionesociale}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Ore</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.5"
                    min="0"
                    value={formData.ore}
                    onChange={(e) => handleChange('ore', e.target.value)}
                    placeholder="Es: 8"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Note</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
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

      {/* Dettagli (Operatori) - Solo in modalità edit */}
      {isEdit && (
        <Card className="shadow-sm">
          <Card.Header className="d-flex justify-content-between align-items-center">
            <span>
              <strong>Operatori Formati</strong>
              <Badge bg="secondary" className="ms-2">
                {dettagli.length}
              </Badge>
            </span>
            <Button variant="success" size="sm" onClick={handleAddDettaglio}>
              <FaPlus className="me-1" /> Aggiungi Operatore
            </Button>
          </Card.Header>
          <Card.Body>
            {dettagli.length === 0 ? (
              <p className="text-muted">Nessun operatore registrato per questa formazione.</p>
            ) : (
              <Table hover responsive bordered>
                <thead className="table-light">
                  <tr>
                    <th>Operatore</th>
                    <th style={{ width: '100px' }}>Presenza</th>
                    <th style={{ width: '80px' }}>Ore</th>
                    <th style={{ width: '120px' }}>Scadenza</th>
                    <th style={{ width: '100px' }}>Certificato</th>
                    <th style={{ width: '100px' }}>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {dettagli.map((d) => (
                    <tr
                      key={d.id}
                      onClick={() => handleEditDettaglio(d.id)}
                      style={{ cursor: 'pointer' }}
                      className="align-middle"
                    >
                      <td className="text-primary">{d.fk_hr_display || '—'}</td>
                      <td>
                        <Badge bg={d.presenza === 'presente' ? 'success' : 'warning'}>
                          {d.presenza === 'presente' ? 'Presente' : 'Assente'}
                        </Badge>
                      </td>
                      <td>{d.ore || '—'}</td>
                      <td>{formatDate(d.scadenza_effettiva)}</td>
                      <td>
                        {d.certificato_url ? (
                          <a
                            href={d.certificato_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            title="Visualizza certificato"
                          >
                            <FaFileAlt className="text-primary" />
                          </a>
                        ) : (
                          <span className="text-muted">—</span>
                        )}
                      </td>
                      <td>
                        <ButtonGroup size="sm">
                          <Button
                            variant="outline-primary"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleEditDettaglio(d.id);
                            }}
                            title="Modifica"
                          >
                            <FaEdit />
                          </Button>
                          <Button
                            variant="outline-danger"
                            onClick={(e) => handleDeleteDettaglioClick(e, d.id)}
                            title="Elimina"
                          >
                            <FaTrash />
                          </Button>
                        </ButtonGroup>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            )}
          </Card.Body>
        </Card>
      )}

      {/* Messaggio per new mode */}
      {!isEdit && (
        <Alert variant="info">
          Salva prima il registro formazione per poter aggiungere gli operatori.
        </Alert>
      )}

      {/* Delete Dettaglio Modal */}
      <Modal show={showDeleteModal} onHide={handleDeleteDettaglioCancel} centered>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Sei sicuro di voler rimuovere questo operatore dalla formazione?
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleDeleteDettaglioCancel}
            disabled={deleteLoading}
          >
            Annulla
          </Button>
          <Button
            variant="danger"
            onClick={handleDeleteDettaglioConfirm}
            disabled={deleteLoading}
          >
            {deleteLoading ? <Spinner animation="border" size="sm" /> : 'Elimina'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}

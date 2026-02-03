/**
 * IncarichiSicurezzaTab - Tab per gestire gli incarichi sicurezza di un dipendente
 *
 * Mostra la lista degli incarichi esistenti e permette di aggiungerne/modificarne.
 * Validazione overlap date gestita dal backend.
 */
import { useState, useEffect, useCallback } from 'react';
import {
  Table,
  Button,
  Spinner,
  Modal,
  Form,
  Row,
  Col,
  Alert,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getHrSafetyByHr,
  createHrSafety,
  updateHrSafety,
  deleteHrSafety,
  getSafetyRoles,
} from '../api';
import type {
  HrSafety,
  HrSafetyCreate,
  SafetyRole,
} from '../types';

interface IncarichiSicurezzaTabProps {
  dipendenteId: number;
  onIncarichiChange?: () => void;
}

export default function IncarichiSicurezzaTab({
  dipendenteId,
  onIncarichiChange,
}: IncarichiSicurezzaTabProps) {
  // Data state
  const [incarichi, setIncarichi] = useState<HrSafety[]>([]);
  const [safetyRoles, setSafetyRoles] = useState<SafetyRole[]>([]);

  // UI state
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingIncarico, setEditingIncarico] = useState<HrSafety | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);

  // Form state
  const [formRole, setFormRole] = useState<number | ''>('');
  const [formDataInizio, setFormDataInizio] = useState('');
  const [formDataFine, setFormDataFine] = useState('');
  const [formNote, setFormNote] = useState('');

  // Carica incarichi del dipendente
  const loadIncarichi = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getHrSafetyByHr(dipendenteId, { page_size: 100 });
      setIncarichi(res.data.results);
    } catch {
      toast.error('Errore caricamento incarichi sicurezza');
    } finally {
      setLoading(false);
    }
  }, [dipendenteId]);

  // Carica safety roles
  const loadSafetyRoles = useCallback(async () => {
    try {
      const res = await getSafetyRoles({ page_size: 1000 });
      setSafetyRoles(res.data.results);
    } catch {
      toast.error('Errore caricamento ruoli sicurezza');
    }
  }, []);

  useEffect(() => {
    loadIncarichi();
    loadSafetyRoles();
  }, [loadIncarichi, loadSafetyRoles]);

  const handleAdd = () => {
    setEditingIncarico(null);
    setFormRole('');
    setFormDataInizio('');
    setFormDataFine('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (incarico: HrSafety) => {
    setEditingIncarico(incarico);
    setFormRole(incarico.fk_safety_role);
    setFormDataInizio(incarico.data_inizio_incarico);
    setFormDataFine(incarico.data_fine_incarico || '');
    setFormNote(incarico.note || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formRole) {
      toast.warning('Seleziona un ruolo sicurezza');
      return;
    }

    if (!formDataInizio) {
      toast.warning('La data inizio è obbligatoria');
      return;
    }

    // Validazione client-side: data fine STRICT > data inizio (blocca intervalli vuoti)
    // Nota: confronto stringhe ISO YYYY-MM-DD funziona correttamente (ordinamento lessicografico)
    if (formDataFine && formDataFine <= formDataInizio) {
      toast.error('La data fine deve essere maggiore della data inizio. Intervalli vuoti (fine = inizio) non sono permessi.');
      return;
    }

    try {
      setSaving(true);
      const data: HrSafetyCreate = {
        fk_hr: dipendenteId,
        fk_safety_role: formRole as number,
        data_inizio_incarico: formDataInizio,
        data_fine_incarico: formDataFine || null,
        note: formNote.trim() || null,
      };

      if (editingIncarico) {
        await updateHrSafety(editingIncarico.id, data);
        toast.success('Incarico aggiornato');
      } else {
        await createHrSafety(data);
        toast.success('Incarico creato');
      }

      setShowModal(false);
      await loadIncarichi();
      onIncarichiChange?.();
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      const nonFieldErrors = err.response?.data?.non_field_errors;

      if (nonFieldErrors && nonFieldErrors.length > 0) {
        toast.error(nonFieldErrors[0]);
      } else if (detail) {
        toast.error(detail);
      } else {
        toast.error('Errore salvataggio incarico');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (incarico: HrSafety) => {
    if (!confirm(`Eliminare l'incarico "${incarico.fk_safety_role_display}"?`)) {
      return;
    }

    try {
      setDeleting(incarico.id);
      await deleteHrSafety(incarico.id);
      toast.success('Incarico eliminato');
      await loadIncarichi();
      onIncarichiChange?.();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore eliminazione incarico';
      toast.error(msg);
    } finally {
      setDeleting(null);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
        <p className="mt-2">Caricamento incarichi...</p>
      </div>
    );
  }

  return (
    <>
      <div className="mb-3">
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Aggiungi Incarico Sicurezza
        </Button>
      </div>

      {incarichi.length === 0 ? (
        <Alert variant="info">
          Nessun incarico sicurezza assegnato a questo dipendente.
        </Alert>
      ) : (
        <Table striped hover responsive>
          <thead>
            <tr>
              <th>Ruolo Sicurezza</th>
              <th>Data Inizio</th>
              <th>Data Fine</th>
              <th>Note</th>
              <th style={{ width: '120px' }}>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {incarichi.map((incarico) => (
              <tr key={incarico.id}>
                <td>{incarico.fk_safety_role_display}</td>
                <td>{new Date(incarico.data_inizio_incarico).toLocaleDateString('it-IT')}</td>
                <td>
                  {incarico.data_fine_incarico
                    ? new Date(incarico.data_fine_incarico).toLocaleDateString('it-IT')
                    : '-'}
                </td>
                <td>{incarico.note || '-'}</td>
                <td>
                  <ButtonGroup size="sm">
                    <Button
                      variant="outline-primary"
                      onClick={() => handleEdit(incarico)}
                      title="Modifica"
                    >
                      ✎
                    </Button>
                    <Button
                      variant="outline-danger"
                      onClick={() => handleDelete(incarico)}
                      disabled={deleting === incarico.id}
                      title="Elimina"
                    >
                      {deleting === incarico.id ? '...' : '✕'}
                    </Button>
                  </ButtonGroup>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Modal per add/edit incarico */}
      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static" size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {editingIncarico ? 'Modifica Incarico Sicurezza' : 'Nuovo Incarico Sicurezza'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Ruolo Sicurezza <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formRole}
                    onChange={(e) => setFormRole(e.target.value ? Number(e.target.value) : '')}
                    required
                  >
                    <option value="">-- Seleziona ruolo --</option>
                    {safetyRoles.map((role) => (
                      <option key={role.id} value={role.id}>
                        {role.descrizione}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Data Inizio Incarico <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    type="date"
                    value={formDataInizio}
                    onChange={(e) => setFormDataInizio(e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Data Fine Incarico (opzionale)</Form.Label>
                  <Form.Control
                    type="date"
                    value={formDataFine}
                    onChange={(e) => setFormDataFine(e.target.value)}
                  />
                  <Form.Text className="text-muted">
                    Lascia vuoto se l'incarico è ancora attivo
                  </Form.Text>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Note (opzionale)</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={formNote}
                    onChange={(e) => setFormNote(e.target.value)}
                  />
                </Form.Group>
              </Col>
            </Row>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)} disabled={saving}>
              Annulla
            </Button>
            <Button variant="primary" type="submit" disabled={saving}>
              {saving ? <Spinner animation="border" size="sm" /> : 'Salva'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
}

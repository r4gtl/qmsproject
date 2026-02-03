/**
 * ValutazioniTab - Tab per gestire le valutazioni di un dipendente
 *
 * Mostra la lista delle valutazioni esistenti e permette di aggiungerne/modificarne.
 * Ogni dipendente può avere al massimo una valutazione per centro di lavoro.
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
  Badge,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getValutazioni,
  createValutazione,
  updateValutazione,
  deleteValutazione,
  getCentriDiLavoro,
} from '../api';
import type {
  ValutazioneOperatore,
  ValutazioneCreate,
  ValutazioneLevel,
  CentrodiLavoro,
} from '../types';
import { VALUTAZIONE_CHOICES } from '../types';

interface ValutazioniTabProps {
  dipendenteId: number;
  onValutazioniChange?: () => void;
}

export default function ValutazioniTab({
  dipendenteId,
  onValutazioniChange,
}: ValutazioniTabProps) {
  // Data state
  const [valutazioni, setValutazioni] = useState<ValutazioneOperatore[]>([]);
  const [centriDiLavoro, setCentriDiLavoro] = useState<CentrodiLavoro[]>([]);

  // UI state
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingValutazione, setEditingValutazione] = useState<ValutazioneOperatore | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);

  // Form state
  const [formCentro, setFormCentro] = useState<number | ''>('');
  const [formValutazione, setFormValutazione] = useState<ValutazioneLevel>('nessuna');
  const [formNote, setFormNote] = useState('');

  // Carica valutazioni del dipendente
  const loadValutazioni = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getValutazioni({ fk_hr: dipendenteId, page_size: 100 });
      setValutazioni(res.data.results);
    } catch {
      toast.error('Errore caricamento valutazioni');
    } finally {
      setLoading(false);
    }
  }, [dipendenteId]);

  // Carica centri di lavoro
  const loadCentri = useCallback(async () => {
    try {
      const res = await getCentriDiLavoro({ page_size: 1000 });
      setCentriDiLavoro(res.data.results);
    } catch {
      toast.error('Errore caricamento centri di lavoro');
    }
  }, []);

  useEffect(() => {
    loadValutazioni();
    loadCentri();
  }, [loadValutazioni, loadCentri]);

  // Centri disponibili (non già associati, a meno che in modifica)
  const centriDisponibili = centriDiLavoro.filter((c) => {
    // Se in modifica, includi il centro corrente
    if (editingValutazione && editingValutazione.fk_centro_di_lavoro === c.id) {
      return true;
    }
    // Altrimenti escludi centri già usati
    return !valutazioni.some((v) => v.fk_centro_di_lavoro === c.id);
  });

  // Apri modal per nuova valutazione
  const handleAdd = () => {
    setEditingValutazione(null);
    setFormCentro('');
    setFormValutazione('nessuna');
    setFormNote('');
    setShowModal(true);
  };

  // Apri modal per modifica
  const handleEdit = (val: ValutazioneOperatore) => {
    setEditingValutazione(val);
    setFormCentro(val.fk_centro_di_lavoro);
    setFormValutazione(val.valutazione);
    setFormNote(val.note || '');
    setShowModal(true);
  };

  // Chiudi modal
  const handleCloseModal = () => {
    setShowModal(false);
    setEditingValutazione(null);
  };

  // Salva valutazione
  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formCentro) {
      toast.warning('Seleziona un centro di lavoro');
      return;
    }

    try {
      setSaving(true);

      const data: ValutazioneCreate = {
        fk_hr: dipendenteId,
        fk_centro_di_lavoro: formCentro as number,
        valutazione: formValutazione,
        note: formNote || null,
      };

      if (editingValutazione) {
        // Update
        await updateValutazione(editingValutazione.id, data);
        toast.success('Valutazione aggiornata');
      } else {
        // Create
        await createValutazione(data);
        toast.success('Valutazione creata');
      }

      handleCloseModal();
      await loadValutazioni();
      onValutazioniChange?.();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  // Elimina valutazione
  const handleDelete = async (val: ValutazioneOperatore) => {
    if (!confirm(`Eliminare la valutazione per "${val.fk_centro_di_lavoro_display}"?`)) {
      return;
    }

    try {
      setDeleting(val.id);
      await deleteValutazione(val.id);
      toast.success('Valutazione eliminata');
      await loadValutazioni();
      onValutazioniChange?.();
    } catch {
      toast.error('Errore eliminazione');
    } finally {
      setDeleting(null);
    }
  };

  // Badge color per valutazione
  const getValutazioneBadge = (val: ValutazioneLevel) => {
    switch (val) {
      case 'massimo':
        return 'success';
      case 'migliore':
        return 'primary';
      case 'medio':
        return 'info';
      case 'minimo':
        return 'warning';
      case 'nessuna':
      default:
        return 'secondary';
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
        <p className="mt-2 text-muted">Caricamento valutazioni...</p>
      </div>
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">Valutazioni per Centro di Lavoro</h5>
        <Button
          variant="primary"
          size="sm"
          onClick={handleAdd}
          disabled={centriDisponibili.length === 0}
        >
          + Nuova Valutazione
        </Button>
      </div>

      {valutazioni.length === 0 ? (
        <p className="text-muted">Nessuna valutazione registrata per questo dipendente.</p>
      ) : (
        <Table striped hover responsive>
          <thead>
            <tr>
              <th>Centro di Lavoro</th>
              <th>Valutazione</th>
              <th>Note</th>
              <th style={{ width: '120px' }}>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {valutazioni.map((val) => (
              <tr key={val.id}>
                <td>{val.fk_centro_di_lavoro_display}</td>
                <td>
                  <Badge bg={getValutazioneBadge(val.valutazione)}>
                    {val.valutazione_display}
                  </Badge>
                </td>
                <td>{val.note || '-'}</td>
                <td>
                  <ButtonGroup size="sm">
                    <Button
                      variant="outline-primary"
                      onClick={() => handleEdit(val)}
                      title="Modifica"
                    >
                      ✎
                    </Button>
                    <Button
                      variant="outline-danger"
                      onClick={() => handleDelete(val)}
                      disabled={deleting === val.id}
                      title="Elimina"
                    >
                      {deleting === val.id ? '...' : '✕'}
                    </Button>
                  </ButtonGroup>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {centriDisponibili.length === 0 && valutazioni.length > 0 && (
        <p className="text-muted small">
          Tutti i centri di lavoro hanno già una valutazione per questo dipendente.
        </p>
      )}

      {/* Modal per create/edit */}
      <Modal show={showModal} onHide={handleCloseModal} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editingValutazione ? 'Modifica Valutazione' : 'Nuova Valutazione'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Centro di Lavoro <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formCentro}
                    onChange={(e) =>
                      setFormCentro(e.target.value ? Number(e.target.value) : '')
                    }
                    disabled={!!editingValutazione}
                    required
                  >
                    <option value="">-- Seleziona centro --</option>
                    {centriDisponibili.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.description}
                      </option>
                    ))}
                  </Form.Select>
                  {editingValutazione && (
                    <Form.Text className="text-muted">
                      Il centro di lavoro non può essere modificato.
                    </Form.Text>
                  )}
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Valutazione <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formValutazione}
                    onChange={(e) =>
                      setFormValutazione(e.target.value as ValutazioneLevel)
                    }
                    required
                  >
                    {VALUTAZIONE_CHOICES.map((c) => (
                      <option key={c.value} value={c.value}>
                        {c.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formNote}
                onChange={(e) => setFormNote(e.target.value)}
                placeholder="Note opzionali..."
              />
            </Form.Group>
          </Modal.Body>

          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal} disabled={saving}>
              Annulla
            </Button>
            <Button variant="primary" type="submit" disabled={saving}>
              {saving ? (
                <Spinner animation="border" size="sm" />
              ) : editingValutazione ? (
                'Salva Modifiche'
              ) : (
                'Crea Valutazione'
              )}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
}

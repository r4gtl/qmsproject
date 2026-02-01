/**
 * DettaglioModal - Modal per creare/modificare una riga di procedura
 *
 * Include la sezione Caratteristiche quando in modalità edit.
 */
import { useState, useEffect } from 'react';
import {
  Modal,
  Form,
  Button,
  Spinner,
  Row,
  Col,
  Alert,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  createDettaglio,
  updateDettaglio,
  getDettaglio,
} from '../../api/procedure';
import { getFasi } from '../../api/articoli';
import type {
  DettaglioProcedura,
  DettaglioProceduraCreate,
} from '../../types/procedure';
import type { FasiLavoro } from '../../types/articoli';
import CaratteristicheSection from './CaratteristicheSection';

interface DettaglioModalProps {
  show: boolean;
  onHide: () => void;
  proceduraId: number;
  dettaglioId?: number | null; // null = creazione, number = modifica
  onSave: (dettaglio: DettaglioProcedura) => void;
}

export default function DettaglioModal({
  show,
  onHide,
  proceduraId,
  dettaglioId,
  onSave,
}: DettaglioModalProps) {
  const isEditMode = !!dettaglioId;

  // Form state
  const [fkFaselavoro, setFkFaselavoro] = useState<number | ''>('');
  const [isInterna, setIsInterna] = useState(true);
  const [note, setNote] = useState('');

  // Data state
  const [fasiLavoro, setFasiLavoro] = useState<FasiLavoro[]>([]);
  const [dettaglio, setDettaglio] = useState<DettaglioProcedura | null>(null);

  // UI state
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  // Carica fasi lavoro
  useEffect(() => {
    const loadFasi = async () => {
      try {
        const res = await getFasi();
        setFasiLavoro(res.data.results || res.data);
      } catch {
        toast.error('Errore caricamento fasi lavoro');
      }
    };
    if (show) {
      loadFasi();
    }
  }, [show]);

  // Carica dettaglio se in edit mode
  useEffect(() => {
    const loadDettaglio = async () => {
      if (!dettaglioId) return;
      try {
        setLoading(true);
        const res = await getDettaglio(dettaglioId);
        const d = res.data;
        setDettaglio(d);
        setFkFaselavoro(d.fk_faselavoro);
        setIsInterna(d.is_interna);
        setNote(d.note || '');
      } catch {
        toast.error('Errore caricamento dettaglio');
      } finally {
        setLoading(false);
      }
    };

    if (show && isEditMode) {
      loadDettaglio();
    } else if (show && !isEditMode) {
      // Reset form per creazione
      setDettaglio(null);
      setFkFaselavoro('');
      setIsInterna(true);
      setNote('');
    }
  }, [show, dettaglioId, isEditMode]);

  // Salva
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!fkFaselavoro) {
      toast.warning('Seleziona una fase di lavoro');
      return;
    }

    try {
      setSaving(true);

      if (isEditMode && dettaglioId) {
        const res = await updateDettaglio(dettaglioId, {
          fk_faselavoro: fkFaselavoro as number,
          is_interna: isInterna,
          note,
        });
        toast.success('Riga aggiornata');
        onSave(res.data);
      } else {
        const data: DettaglioProceduraCreate = {
          fk_procedura: proceduraId,
          fk_faselavoro: fkFaselavoro as number,
          is_interna: isInterna,
          note,
        };
        const res = await createDettaglio(data);
        toast.success('Riga creata');
        onSave(res.data);
      }

      onHide();
    } catch {
      toast.error('Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  // Callback per aggiornamento caratteristiche (ricarica dettaglio)
  const handleCaratteristicheChange = async () => {
    if (!dettaglioId) return;
    try {
      const res = await getDettaglio(dettaglioId);
      setDettaglio(res.data);
    } catch {
      // ignore
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title>
          {isEditMode ? 'Modifica Riga' : 'Nuova Riga'}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {loading ? (
          <div className="text-center py-4">
            <Spinner animation="border" />
          </div>
        ) : (
          <>
            <Form onSubmit={handleSubmit}>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Fase Lavoro *</Form.Label>
                    <Form.Select
                      value={fkFaselavoro}
                      onChange={(e) =>
                        setFkFaselavoro(
                          e.target.value ? Number(e.target.value) : ''
                        )
                      }
                      required
                    >
                      <option value="">-- Seleziona --</option>
                      {fasiLavoro.map((f) => (
                        <option key={f.id} value={f.id}>
                          {f.descrizione}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Tipo Lavorazione</Form.Label>
                    <div>
                      <Form.Check
                        inline
                        type="radio"
                        label="Interna"
                        name="tipoLavorazione"
                        checked={isInterna}
                        onChange={() => setIsInterna(true)}
                      />
                      <Form.Check
                        inline
                        type="radio"
                        label="Esterna (Terzista)"
                        name="tipoLavorazione"
                        checked={!isInterna}
                        onChange={() => setIsInterna(false)}
                      />
                    </div>
                  </Form.Group>
                </Col>
              </Row>

              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                />
              </Form.Group>

              <div className="text-end">
                <Button
                  variant="secondary"
                  onClick={onHide}
                  className="me-2"
                  disabled={saving}
                >
                  Annulla
                </Button>
                <Button variant="primary" type="submit" disabled={saving}>
                  {saving ? (
                    <Spinner animation="border" size="sm" />
                  ) : isEditMode ? (
                    'Salva Modifiche'
                  ) : (
                    'Crea Riga'
                  )}
                </Button>
              </div>
            </Form>

            {/* Sezione Caratteristiche - solo in edit mode */}
            {isEditMode && dettaglio && (
              <>
                <hr className="my-4" />
                <Alert variant="info" className="mb-3">
                  {isInterna ? (
                    <>
                      <strong>Lavorazione Interna:</strong> Le caratteristiche
                      useranno i <em>Dettagli Fase Lavoro</em>.
                    </>
                  ) : (
                    <>
                      <strong>Lavorazione Esterna:</strong> Le caratteristiche
                      useranno <em>Fornitore</em> e{' '}
                      <em>Lavorazione Esterna</em>.
                    </>
                  )}
                </Alert>
                <CaratteristicheSection
                  dettaglio={dettaglio}
                  onCaratteristicheChange={handleCaratteristicheChange}
                />
              </>
            )}
          </>
        )}
      </Modal.Body>
    </Modal>
  );
}

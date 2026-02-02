/**
 * DettaglioModal - Modal per creare/modificare una riga di procedura
 *
 * Form fields:
 * - fk_faselavoro (select, obbligatorio)
 * - is_interna (radio)
 * - fk_fornitore (select, obbligatorio se is_interna=false)
 * - note (textarea)
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
import instance from '@/api/axios';
import type {
  DettaglioProcedura,
  DettaglioProceduraCreate,
} from '../../types/procedure';
import type { FasiLavoro } from '../../types/articoli';
import CaratteristicheSection from './CaratteristicheSection';

// Tipo per fornitore (API: /anagrafiche/fornitori/)
interface Fornitore {
  id: number;
  ragionesociale: string;
}

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
  const [fkFornitore, setFkFornitore] = useState<number | ''>('');
  const [note, setNote] = useState('');

  // Data state (lookup)
  const [fasiLavoro, setFasiLavoro] = useState<FasiLavoro[]>([]);
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [dettaglio, setDettaglio] = useState<DettaglioProcedura | null>(null);

  // UI state
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loadingLookups, setLoadingLookups] = useState(false);

  // Carica fasi lavoro e fornitori
  useEffect(() => {
    const loadLookups = async () => {
      if (!show) return;
      try {
        setLoadingLookups(true);
        const [fasiRes, fornitoriRes] = await Promise.all([
          getFasi(),
          instance.get('/anagrafiche/fornitori/', { params: { page_size: 1000 } }),
        ]);
        setFasiLavoro(fasiRes.data.results || fasiRes.data);
        setFornitori(fornitoriRes.data.results || fornitoriRes.data);
      } catch {
        toast.error('Errore caricamento dati lookup');
      } finally {
        setLoadingLookups(false);
      }
    };
    loadLookups();
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
        setFkFornitore(d.fk_fornitore || '');
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
      setFkFornitore('');
      setNote('');
    }
  }, [show, dettaglioId, isEditMode]);

  // Validazione form
  const validateForm = (): boolean => {
    if (!fkFaselavoro) {
      toast.warning('Seleziona una fase di lavoro');
      return false;
    }
    // Se lavorazione esterna, fornitore obbligatorio
    if (!isInterna && !fkFornitore) {
      toast.warning('Per lavorazione esterna, seleziona un fornitore');
      return false;
    }
    return true;
  };

  // Salva (create o update)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      setSaving(true);

      if (isEditMode && dettaglioId) {
        // UPDATE
        const res = await updateDettaglio(dettaglioId, {
          fk_faselavoro: fkFaselavoro as number,
          is_interna: isInterna,
          fk_fornitore: isInterna ? null : (fkFornitore as number),
          note: note || undefined,
        });
        toast.success('Riga aggiornata');
        onSave(res.data);
      } else {
        // CREATE
        const data: DettaglioProceduraCreate = {
          fk_procedura: proceduraId,
          fk_faselavoro: fkFaselavoro as number,
          is_interna: isInterna,
          fk_fornitore: isInterna ? undefined : (fkFornitore as number),
          note: note || undefined,
        };
        const res = await createDettaglio(data);
        toast.success('Riga creata');
        onSave(res.data);
      }

      onHide();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
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
      // silent fail
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
        {loading || loadingLookups ? (
          <div className="text-center py-4">
            <Spinner animation="border" />
            <p className="mt-2 text-muted">Caricamento...</p>
          </div>
        ) : (
          <>
            <Form onSubmit={handleSubmit}>
              <Row>
                {/* Fase Lavoro - obbligatorio */}
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>
                      Fase Lavoro <span className="text-danger">*</span>
                    </Form.Label>
                    <Form.Select
                      value={fkFaselavoro}
                      onChange={(e) =>
                        setFkFaselavoro(
                          e.target.value ? Number(e.target.value) : ''
                        )
                      }
                      required
                    >
                      <option value="">-- Seleziona fase --</option>
                      {fasiLavoro.map((f) => (
                        <option key={f.id} value={f.id}>
                          {f.descrizione}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>
                </Col>

                {/* Tipo Lavorazione */}
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Tipo Lavorazione</Form.Label>
                    <div className="mt-2">
                      <Form.Check
                        inline
                        type="radio"
                        id="tipoInterna"
                        label="Interna"
                        name="tipoLavorazione"
                        checked={isInterna}
                        onChange={() => {
                          setIsInterna(true);
                          setFkFornitore(''); // Reset fornitore
                        }}
                      />
                      <Form.Check
                        inline
                        type="radio"
                        id="tipoEsterna"
                        label="Esterna (Terzista)"
                        name="tipoLavorazione"
                        checked={!isInterna}
                        onChange={() => setIsInterna(false)}
                      />
                    </div>
                  </Form.Group>
                </Col>
              </Row>

              {/* Fornitore - visibile e obbligatorio solo se esterna */}
              {!isInterna && (
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>
                        Fornitore <span className="text-danger">*</span>
                      </Form.Label>
                      <Form.Select
                        value={fkFornitore}
                        onChange={(e) =>
                          setFkFornitore(
                            e.target.value ? Number(e.target.value) : ''
                          )
                        }
                        required={!isInterna}
                      >
                        <option value="">-- Seleziona fornitore --</option>
                        {fornitori.map((f) => (
                          <option key={f.id} value={f.id}>
                            {f.ragionesociale}
                          </option>
                        ))}
                      </Form.Select>
                      <Form.Text className="text-muted">
                        Obbligatorio per lavorazione esterna
                      </Form.Text>
                    </Form.Group>
                  </Col>
                </Row>
              )}

              {/* Note */}
              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="Note opzionali sulla riga..."
                />
              </Form.Group>

              {/* Pulsanti */}
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
                <Alert variant={isInterna ? 'info' : 'warning'} className="mb-3">
                  {isInterna ? (
                    <>
                      <strong>Lavorazione Interna:</strong> Le caratteristiche
                      useranno gli <em>Attributi della Fase Lavoro</em>.
                    </>
                  ) : (
                    <>
                      <strong>Lavorazione Esterna:</strong> Le caratteristiche
                      useranno <em>Fornitore</em> e <em>Lavorazione Esterna</em>.
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

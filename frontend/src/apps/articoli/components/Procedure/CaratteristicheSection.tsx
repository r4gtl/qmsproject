/**
 * CaratteristicheSection - Gestione caratteristiche di una riga procedura
 *
 * Visualizza e permette CRUD delle caratteristiche.
 * Adatta i campi in base a is_interna del dettaglio padre.
 */
import { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Form,
  Spinner,
  Badge,
  InputGroup,
  Row,
  Col,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  createCaratteristica,
  updateCaratteristica,
  deleteCaratteristica,
} from '../../api/procedure';
import { getDettagliFase, getLavorazioniEsterne } from '../../api/articoli';
import type {
  DettaglioProcedura,
  CaratteristicaProcedura,
  CaratteristicaProceduraCreate,
} from '../../types/procedure';
import type { DettaglioFaseLavoro, LavorazioneEsterna } from '../../types/articoli';

// API mancante: fornitori
import instance from '@/api/axios';

interface CaratteristicheSectionProps {
  dettaglio: DettaglioProcedura;
  onCaratteristicheChange: () => void;
}

interface Fornitore {
  id: number;
  ragionesociale: string;
}

export default function CaratteristicheSection({
  dettaglio,
  onCaratteristicheChange,
}: CaratteristicheSectionProps) {
  const isInterna = dettaglio.is_interna;

  // Lookup data
  const [dettagliFase, setDettagliFase] = useState<DettaglioFaseLavoro[]>([]);
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [lavorazioniEsterne, setLavorazioniEsterne] = useState<LavorazioneEsterna[]>([]);

  // Form state per nuova caratteristica
  const [newCaratteristica, setNewCaratteristica] = useState<{
    fk_dettaglio_fase_lavoro: number | '';
    fk_fornitore: number | '';
    fk_lavorazione_esterna: number | '';
    valore: string;
    note: string;
  }>({
    fk_dettaglio_fase_lavoro: '',
    fk_fornitore: '',
    fk_lavorazione_esterna: '',
    valore: '',
    note: '',
  });

  // UI state
  const [adding, setAdding] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState('');

  // Carica lookup data
  useEffect(() => {
    const loadLookups = async () => {
      try {
        if (isInterna) {
          // Carica dettagli fase lavoro
          const res = await getDettagliFase(dettaglio.fk_faselavoro);
          setDettagliFase(res.data.results || res.data);
        } else {
          // Carica fornitori e lavorazioni esterne
          const [fornitoriRes, lavEstRes] = await Promise.all([
            instance.get('/anagrafiche/fornitori/', { params: { page_size: 1000 } }),
            getLavorazioniEsterne(),
          ]);
          setFornitori(fornitoriRes.data.results || fornitoriRes.data);
          setLavorazioniEsterne(lavEstRes.data.results || lavEstRes.data);
        }
      } catch {
        toast.error('Errore caricamento dati');
      }
    };
    loadLookups();
  }, [isInterna, dettaglio.fk_faselavoro]);

  // Reset form
  const resetForm = () => {
    setNewCaratteristica({
      fk_dettaglio_fase_lavoro: '',
      fk_fornitore: '',
      fk_lavorazione_esterna: '',
      valore: '',
      note: '',
    });
  };

  // Aggiungi caratteristica
  const handleAdd = async () => {
    // Validazione
    if (isInterna && !newCaratteristica.fk_dettaglio_fase_lavoro) {
      toast.warning('Seleziona un attributo fase');
      return;
    }
    if (!isInterna) {
      if (!newCaratteristica.fk_fornitore) {
        toast.warning('Seleziona un fornitore');
        return;
      }
      if (!newCaratteristica.fk_lavorazione_esterna) {
        toast.warning('Seleziona una lavorazione esterna');
        return;
      }
    }

    try {
      setAdding(true);
      const data: CaratteristicaProceduraCreate = {
        fk_dettaglio_procedura: dettaglio.id,
        valore: newCaratteristica.valore || undefined,
        note: newCaratteristica.note || undefined,
      };

      if (isInterna) {
        data.fk_dettaglio_fase_lavoro = newCaratteristica.fk_dettaglio_fase_lavoro as number;
      } else {
        data.fk_fornitore = newCaratteristica.fk_fornitore as number;
        data.fk_lavorazione_esterna = newCaratteristica.fk_lavorazione_esterna as number;
      }

      await createCaratteristica(data);
      toast.success('Caratteristica aggiunta');
      resetForm();
      onCaratteristicheChange();
    } catch {
      toast.error('Errore aggiunta caratteristica');
    } finally {
      setAdding(false);
    }
  };

  // Modifica valore inline
  const handleSaveEdit = async (car: CaratteristicaProcedura) => {
    try {
      await updateCaratteristica(car.id, { valore: editValue });
      toast.success('Valore aggiornato');
      setEditingId(null);
      onCaratteristicheChange();
    } catch {
      toast.error('Errore aggiornamento');
    }
  };

  // Elimina caratteristica
  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa caratteristica?')) return;
    try {
      await deleteCaratteristica(id);
      toast.success('Caratteristica eliminata');
      onCaratteristicheChange();
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  return (
    <div>
      <h6>Caratteristiche</h6>

      {/* Form nuova caratteristica */}
      <div className="bg-light p-3 rounded mb-3">
        <Row className="g-2 align-items-end">
          {isInterna ? (
            <Col md={4}>
              <Form.Label className="small">Attributo Fase *</Form.Label>
              <Form.Select
                size="sm"
                value={newCaratteristica.fk_dettaglio_fase_lavoro}
                onChange={(e) =>
                  setNewCaratteristica({
                    ...newCaratteristica,
                    fk_dettaglio_fase_lavoro: e.target.value
                      ? Number(e.target.value)
                      : '',
                  })
                }
              >
                <option value="">-- Seleziona --</option>
                {dettagliFase.map((df) => (
                  <option key={df.id} value={df.id}>
                    {df.attributo}
                  </option>
                ))}
              </Form.Select>
            </Col>
          ) : (
            <>
              <Col md={3}>
                <Form.Label className="small">Fornitore *</Form.Label>
                <Form.Select
                  size="sm"
                  value={newCaratteristica.fk_fornitore}
                  onChange={(e) =>
                    setNewCaratteristica({
                      ...newCaratteristica,
                      fk_fornitore: e.target.value
                        ? Number(e.target.value)
                        : '',
                    })
                  }
                >
                  <option value="">-- Seleziona --</option>
                  {fornitori.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.ragionesociale}
                    </option>
                  ))}
                </Form.Select>
              </Col>
              <Col md={3}>
                <Form.Label className="small">Lavorazione Est. *</Form.Label>
                <Form.Select
                  size="sm"
                  value={newCaratteristica.fk_lavorazione_esterna}
                  onChange={(e) =>
                    setNewCaratteristica({
                      ...newCaratteristica,
                      fk_lavorazione_esterna: e.target.value
                        ? Number(e.target.value)
                        : '',
                    })
                  }
                >
                  <option value="">-- Seleziona --</option>
                  {lavorazioniEsterne.map((l) => (
                    <option key={l.id} value={l.id}>
                      {l.descrizione}
                    </option>
                  ))}
                </Form.Select>
              </Col>
            </>
          )}
          <Col md={isInterna ? 3 : 2}>
            <Form.Label className="small">Valore</Form.Label>
            <Form.Control
              size="sm"
              value={newCaratteristica.valore}
              onChange={(e) =>
                setNewCaratteristica({
                  ...newCaratteristica,
                  valore: e.target.value,
                })
              }
              placeholder="es: 100°C"
            />
          </Col>
          <Col md={isInterna ? 3 : 2}>
            <Form.Label className="small">Note</Form.Label>
            <Form.Control
              size="sm"
              value={newCaratteristica.note}
              onChange={(e) =>
                setNewCaratteristica({
                  ...newCaratteristica,
                  note: e.target.value,
                })
              }
            />
          </Col>
          <Col md={2}>
            <Button
              variant="success"
              size="sm"
              onClick={handleAdd}
              disabled={adding}
              className="w-100"
            >
              {adding ? <Spinner animation="border" size="sm" /> : '+ Aggiungi'}
            </Button>
          </Col>
        </Row>
      </div>

      {/* Tabella caratteristiche esistenti */}
      {dettaglio.caratteristiche.length === 0 ? (
        <p className="text-muted small">Nessuna caratteristica.</p>
      ) : (
        <Table size="sm" bordered hover>
          <thead className="table-light">
            <tr>
              <th>#</th>
              {isInterna ? (
                <th>Attributo</th>
              ) : (
                <>
                  <th>Fornitore</th>
                  <th>Lavorazione</th>
                </>
              )}
              <th>Valore</th>
              <th>Note</th>
              <th style={{ width: '80px' }}>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {dettaglio.caratteristiche.map((car) => (
              <tr key={car.id}>
                <td>
                  <Badge bg="secondary">{car.numero_riga}</Badge>
                </td>
                {isInterna ? (
                  <td>{car.fk_dettaglio_fase_lavoro_attributo || '-'}</td>
                ) : (
                  <>
                    <td>{car.fk_fornitore_nome || '-'}</td>
                    <td>{car.fk_lavorazione_esterna_descrizione || '-'}</td>
                  </>
                )}
                <td>
                  {editingId === car.id ? (
                    <InputGroup size="sm">
                      <Form.Control
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleSaveEdit(car);
                          if (e.key === 'Escape') setEditingId(null);
                        }}
                        autoFocus
                      />
                      <Button
                        variant="outline-success"
                        onClick={() => handleSaveEdit(car)}
                      >
                        ✓
                      </Button>
                    </InputGroup>
                  ) : (
                    <span
                      style={{ cursor: 'pointer' }}
                      onClick={() => {
                        setEditingId(car.id);
                        setEditValue(car.valore || '');
                      }}
                      title="Click per modificare"
                    >
                      {car.valore || <em className="text-muted">-</em>}
                    </span>
                  )}
                </td>
                <td className="text-truncate" style={{ maxWidth: '150px' }}>
                  {car.note || '-'}
                </td>
                <td>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(car.id)}
                  >
                    ✕
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

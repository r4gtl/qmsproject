/**
 * CaratteristicheSection - Gestione caratteristiche con DnD
 *
 * Funzionalità:
 * - CRUD caratteristiche (create, inline edit valore, delete)
 * - Drag&Drop per riordinare (usa @dnd-kit)
 * - Optimistic update con rollback su errore
 *
 * HARDENING:
 * - Rollback usa backup locale (no stale closure)
 * - Handle con stopPropagation (evita click accidentale)
 * - Sync con response API dopo reorder OK
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

// @dnd-kit imports
import {
  DndContext,
  closestCenter,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

import {
  createCaratteristica,
  updateCaratteristica,
  deleteCaratteristica,
  reorderCaratteristiche,
} from '../../api/procedure';
import { getDettagliFase, getLavorazioniEsterne } from '../../api/articoli';
import type {
  DettaglioProcedura,
  CaratteristicaProcedura,
  CaratteristicaProceduraCreate,
} from '../../types/procedure';
import type { DettaglioFaseLavoro, LavorazioneEsterna } from '../../types/articoli';

import instance from '@/api/axios';

// =============================================================================
// TYPES
// =============================================================================

interface CaratteristicheSectionProps {
  dettaglio: DettaglioProcedura;
  onCaratteristicheChange: () => void;
}

interface Fornitore {
  id: number;
  ragionesociale: string;
}

// =============================================================================
// SORTABLE ROW COMPONENT
// =============================================================================

interface SortableCaratteristicaRowProps {
  car: CaratteristicaProcedura;
  index: number;
  isInterna: boolean;
  editingId: number | null;
  editValue: string;
  setEditingId: (id: number | null) => void;
  setEditValue: (v: string) => void;
  onSaveEdit: (car: CaratteristicaProcedura) => void;
  onDelete: (id: number) => void;
  isDragDisabled: boolean;
}

function SortableCaratteristicaRow({
  car,
  index,
  isInterna,
  editingId,
  editValue,
  setEditingId,
  setEditValue,
  onSaveEdit,
  onDelete,
  isDragDisabled,
}: SortableCaratteristicaRowProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: car.id,
    disabled: isDragDisabled,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    backgroundColor: isDragging ? '#f8f9fa' : undefined,
  };

  /**
   * HARDENING: stopPropagation sull'handle
   * Evita che eventi sull'handle propaghino e causino effetti indesiderati.
   */
  const handlePointerDown = (e: React.PointerEvent) => {
    e.stopPropagation();
  };
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  return (
    <tr ref={setNodeRef} style={style}>
      {/* Handle drag */}
      <td
        {...attributes}
        {...listeners}
        onPointerDown={handlePointerDown}
        onClick={handleClick}
        style={{
          width: '30px',
          cursor: isDragDisabled ? 'not-allowed' : 'grab',
          textAlign: 'center',
          userSelect: 'none',
        }}
        title={isDragDisabled ? 'Riordino in corso...' : 'Trascina per riordinare'}
      >
        <span style={{ opacity: isDragDisabled ? 0.5 : 1 }}>☰</span>
      </td>

      {/* Numero riga */}
      <td>
        <Badge bg="secondary">{index + 1}</Badge>
      </td>

      {/* Colonne per interna/esterna */}
      {isInterna ? (
        <td>{car.fk_dettaglio_fase_lavoro_attributo || '-'}</td>
      ) : (
        <>
          <td>{car.fk_fornitore_nome || '-'}</td>
          <td>{car.fk_lavorazione_esterna_descrizione || '-'}</td>
        </>
      )}

      {/* Valore - inline edit */}
      <td>
        {editingId === car.id ? (
          <InputGroup size="sm">
            <Form.Control
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') onSaveEdit(car);
                if (e.key === 'Escape') setEditingId(null);
              }}
              autoFocus
            />
            <Button
              variant="outline-success"
              onClick={() => onSaveEdit(car)}
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

      {/* Note */}
      <td className="text-truncate" style={{ maxWidth: '150px' }}>
        {car.note || '-'}
      </td>

      {/* Azioni */}
      <td style={{ width: '60px' }}>
        <Button
          variant="outline-danger"
          size="sm"
          onClick={() => onDelete(car.id)}
        >
          ✕
        </Button>
      </td>
    </tr>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function CaratteristicheSection({
  dettaglio,
  onCaratteristicheChange,
}: CaratteristicheSectionProps) {
  const isInterna = dettaglio.is_interna;

  // Local state per caratteristiche (per optimistic update)
  const [localCaratteristiche, setLocalCaratteristiche] = useState<CaratteristicaProcedura[]>(
    dettaglio.caratteristiche || []
  );

  // Sync con parent
  useEffect(() => {
    setLocalCaratteristiche(dettaglio.caratteristiche || []);
  }, [dettaglio.caratteristiche]);

  // Lookup data
  const [dettagliFase, setDettagliFase] = useState<DettaglioFaseLavoro[]>([]);
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [lavorazioniEsterne, setLavorazioniEsterne] = useState<LavorazioneEsterna[]>([]);

  // Form state
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
  const [isReordering, setIsReordering] = useState(false);

  // Sensors
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        if (isInterna) {
          const res = await getDettagliFase(dettaglio.fk_faselavoro);
          setDettagliFase(res.data.results || res.data);
        } else {
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

  // Add caratteristica
  const handleAdd = async () => {
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

  // Edit valore inline
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

  // Delete
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

  /**
   * REORDER con optimistic update + rollback
   *
   * HARDENING: usa backup locale (const) invece di state
   * per evitare stale closure nel catch.
   */
  const handleReorder = async (newCaratteristiche: CaratteristicaProcedura[]) => {
    // BACKUP LOCALE - catturato PRIMA di qualsiasi modifica
    const backup = [...localCaratteristiche];

    // Optimistic update
    setLocalCaratteristiche(newCaratteristiche);
    setIsReordering(true);

    try {
      const orderedIds = newCaratteristiche.map((c) => c.id);
      const response = await reorderCaratteristiche(dettaglio.id, orderedIds);

      /**
       * SYNC con response API:
       * L'API ritorna CaratteristicaProcedura[] con numero_riga aggiornato.
       * Usiamo la response per sincronizzare lo state con i dati server.
       */
      if (response.data && Array.isArray(response.data)) {
        setLocalCaratteristiche(response.data);
      }
      // Se API non ritorna array, l'ordine locale è già corretto
    } catch {
      // ROLLBACK: usa backup locale (no stale closure)
      toast.error('Errore riordino, ripristinato ordine precedente');
      setLocalCaratteristiche(backup);
    } finally {
      setIsReordering(false);
    }
  };

  // Drag end
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over || active.id === over.id) return;

    const oldIndex = localCaratteristiche.findIndex((c) => c.id === active.id);
    const newIndex = localCaratteristiche.findIndex((c) => c.id === over.id);

    if (oldIndex === -1 || newIndex === -1) return;

    const newCaratteristiche = arrayMove(localCaratteristiche, oldIndex, newIndex);
    handleReorder(newCaratteristiche);
  };

  return (
    <div>
      <h6>
        Caratteristiche
        {isReordering && (
          <Spinner animation="border" size="sm" className="ms-2" />
        )}
      </h6>

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

      {/* Tabella con DnD */}
      {localCaratteristiche.length === 0 ? (
        <p className="text-muted small">Nessuna caratteristica.</p>
      ) : (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={localCaratteristiche.map((c) => c.id)}
            strategy={verticalListSortingStrategy}
          >
            <Table size="sm" bordered hover>
              <thead className="table-light">
                <tr>
                  <th style={{ width: '30px' }}></th>
                  <th style={{ width: '40px' }}>#</th>
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
                  <th style={{ width: '60px' }}>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {localCaratteristiche.map((car, idx) => (
                  <SortableCaratteristicaRow
                    key={car.id}
                    car={car}
                    index={idx}
                    isInterna={isInterna}
                    editingId={editingId}
                    editValue={editValue}
                    setEditingId={setEditingId}
                    setEditValue={setEditValue}
                    onSaveEdit={handleSaveEdit}
                    onDelete={handleDelete}
                    isDragDisabled={isReordering}
                  />
                ))}
              </tbody>
            </Table>
          </SortableContext>
        </DndContext>
      )}
    </div>
  );
}

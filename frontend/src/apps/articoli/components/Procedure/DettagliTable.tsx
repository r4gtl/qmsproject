/**
 * DettagliTable - Tabella righe procedura con drag&drop
 *
 * Usa @dnd-kit per il reorder delle righe.
 * Fallback con pulsanti su/giù per accessibilità.
 */
import { useState, useCallback } from 'react';
import { Table, Button, Badge, Spinner, ButtonGroup } from 'react-bootstrap';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { toast } from 'react-toastify';
import { reorderDettagliProcedura, deleteDettaglio } from '../../api/procedure';
import type { DettaglioProcedura } from '../../types/procedure';

interface DettagliTableProps {
  proceduraId: number;
  dettagli: DettaglioProcedura[];
  onDettagliChange: (dettagli: DettaglioProcedura[]) => void;
  onRowClick: (dettaglio: DettaglioProcedura) => void;
  onAddClick: () => void;
}

// Componente riga sortable
interface SortableRowProps {
  dettaglio: DettaglioProcedura;
  onRowClick: (d: DettaglioProcedura) => void;
  onDelete: (id: number) => void;
  onMoveUp: (id: number) => void;
  onMoveDown: (id: number) => void;
  isFirst: boolean;
  isLast: boolean;
}

function SortableRow({
  dettaglio,
  onRowClick,
  onDelete,
  onMoveUp,
  onMoveDown,
  isFirst,
  isLast,
}: SortableRowProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: dettaglio.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    cursor: 'grab',
  };

  return (
    <tr ref={setNodeRef} style={style} className="align-middle">
      {/* Handle drag */}
      <td {...attributes} {...listeners} style={{ width: '40px' }}>
        <span style={{ cursor: 'grab' }}>☰</span>
      </td>
      {/* Numero riga */}
      <td style={{ width: '60px' }}>
        <Badge bg="secondary">{dettaglio.numero_riga}</Badge>
      </td>
      {/* Fase lavoro */}
      <td
        onClick={() => onRowClick(dettaglio)}
        style={{ cursor: 'pointer' }}
      >
        {dettaglio.fk_faselavoro_descrizione || `ID: ${dettaglio.fk_faselavoro}`}
      </td>
      {/* Tipo */}
      <td style={{ width: '100px' }}>
        <Badge bg={dettaglio.is_interna ? 'success' : 'warning'}>
          {dettaglio.is_interna ? 'Interna' : 'Esterna'}
        </Badge>
      </td>
      {/* Fornitore (se esterna) */}
      <td>
        {!dettaglio.is_interna && dettaglio.fk_fornitore_nome
          ? dettaglio.fk_fornitore_nome
          : '-'}
      </td>
      {/* Caratteristiche count */}
      <td style={{ width: '80px' }}>
        <Badge bg="info">{dettaglio.caratteristiche_count}</Badge>
      </td>
      {/* Azioni */}
      <td style={{ width: '150px' }}>
        <ButtonGroup size="sm">
          <Button
            variant="outline-secondary"
            disabled={isFirst}
            onClick={() => onMoveUp(dettaglio.id)}
            title="Sposta su"
          >
            ↑
          </Button>
          <Button
            variant="outline-secondary"
            disabled={isLast}
            onClick={() => onMoveDown(dettaglio.id)}
            title="Sposta giù"
          >
            ↓
          </Button>
          <Button
            variant="outline-danger"
            onClick={() => onDelete(dettaglio.id)}
            title="Elimina"
          >
            ✕
          </Button>
        </ButtonGroup>
      </td>
    </tr>
  );
}

export default function DettagliTable({
  proceduraId,
  dettagli,
  onDettagliChange,
  onRowClick,
  onAddClick,
}: DettagliTableProps) {
  const [saving, setSaving] = useState(false);
  // Salva l'ordine precedente per rollback in caso di errore
  const [previousOrder, setPreviousOrder] = useState<DettaglioProcedura[] | null>(null);

  // Sensori per dnd-kit
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Salva l'ordine sul server con rollback ottimistico
  const saveOrder = useCallback(
    async (newDettagli: DettaglioProcedura[], oldDettagli: DettaglioProcedura[]) => {
      // Aggiorna subito la UI (optimistic update)
      const optimisticUpdated = newDettagli.map((d, idx) => ({
        ...d,
        numero_riga: idx + 1,
      }));
      onDettagliChange(optimisticUpdated);
      setPreviousOrder(oldDettagli);

      try {
        setSaving(true);
        const orderedIds = newDettagli.map((d) => d.id);
        await reorderDettagliProcedura(proceduraId, orderedIds);
        // Successo: pulisci il backup
        setPreviousOrder(null);
      } catch {
        toast.error('Errore nel salvataggio ordine - ripristino...');
        // Rollback all'ordine precedente
        onDettagliChange(oldDettagli);
        setPreviousOrder(null);
      } finally {
        setSaving(false);
      }
    },
    [proceduraId, onDettagliChange]
  );

  // Gestisce fine drag
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    const oldIndex = dettagli.findIndex((d) => d.id === active.id);
    const newIndex = dettagli.findIndex((d) => d.id === over.id);

    const newDettagli = arrayMove(dettagli, oldIndex, newIndex);
    saveOrder(newDettagli, dettagli);
  };

  // Sposta su
  const handleMoveUp = (id: number) => {
    const idx = dettagli.findIndex((d) => d.id === id);
    if (idx <= 0) return;
    const newDettagli = arrayMove(dettagli, idx, idx - 1);
    saveOrder(newDettagli, dettagli);
  };

  // Sposta giù
  const handleMoveDown = (id: number) => {
    const idx = dettagli.findIndex((d) => d.id === id);
    if (idx < 0 || idx >= dettagli.length - 1) return;
    const newDettagli = arrayMove(dettagli, idx, idx + 1);
    saveOrder(newDettagli, dettagli);
  };

  // Elimina riga
  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa riga?')) return;
    try {
      await deleteDettaglio(id);
      const newDettagli = dettagli.filter((d) => d.id !== id);
      onDettagliChange(newDettagli);
      toast.success('Riga eliminata');
    } catch {
      toast.error('Errore eliminazione riga');
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">
          Righe Procedura{' '}
          {saving && <Spinner animation="border" size="sm" className="ms-2" />}
        </h5>
        <Button variant="primary" size="sm" onClick={onAddClick}>
          + Aggiungi Riga
        </Button>
      </div>

      {dettagli.length === 0 ? (
        <p className="text-muted">Nessuna riga. Clicca "Aggiungi Riga" per iniziare.</p>
      ) : (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={dettagli.map((d) => d.id)}
            strategy={verticalListSortingStrategy}
          >
            <Table hover responsive bordered>
              <thead className="table-light">
                <tr>
                  <th style={{ width: '40px' }}></th>
                  <th style={{ width: '60px' }}>#</th>
                  <th>Fase Lavoro</th>
                  <th style={{ width: '100px' }}>Tipo</th>
                  <th>Fornitore</th>
                  <th style={{ width: '80px' }}>Caratt.</th>
                  <th style={{ width: '150px' }}>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {dettagli.map((d, idx) => (
                  <SortableRow
                    key={d.id}
                    dettaglio={d}
                    onRowClick={onRowClick}
                    onDelete={handleDelete}
                    onMoveUp={handleMoveUp}
                    onMoveDown={handleMoveDown}
                    isFirst={idx === 0}
                    isLast={idx === dettagli.length - 1}
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

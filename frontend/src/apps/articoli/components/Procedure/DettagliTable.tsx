/**
 * DettagliTable - Tabella righe procedura con Drag&Drop
 *
 * Funzionalità:
 * - Visualizza righe di una procedura (DettaglioProcedura)
 * - Drag&Drop per riordinare (usa @dnd-kit)
 * - Optimistic update con rollback su errore
 * - CRUD: click per edit, delete con conferma
 *
 * HARDENING:
 * - Rollback usa backup locale (no stale closure)
 * - Handle con stopPropagation (evita click accidentale su riga)
 * - Sync con response API dopo reorder OK
 */
import { useState } from 'react';
import { Table, Button, Badge, ButtonGroup, Spinner } from 'react-bootstrap';
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

import { deleteDettaglio, reorderDettagliProcedura } from '../../api/procedure';
import type { DettaglioProcedura } from '../../types/procedure';

// =============================================================================
// PROPS
// =============================================================================

interface DettagliTableProps {
  proceduraId: number;
  dettagli: DettaglioProcedura[];
  onDettagliChange: (dettagli: DettaglioProcedura[]) => void;
  onRowClick: (dettaglio: DettaglioProcedura) => void;
  onAddClick: () => void;
}

// =============================================================================
// SORTABLE ROW COMPONENT
// =============================================================================

interface SortableRowProps {
  dettaglio: DettaglioProcedura;
  index: number;
  onRowClick: (d: DettaglioProcedura) => void;
  onDelete: (id: number) => void;
  deleting: number | null;
  isDragDisabled: boolean;
}

function SortableRow({
  dettaglio,
  index,
  onRowClick,
  onDelete,
  deleting,
  isDragDisabled,
}: SortableRowProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: dettaglio.id,
    disabled: isDragDisabled,
  });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    backgroundColor: isDragging ? '#f8f9fa' : undefined,
  };

  /**
   * HARDENING: stopPropagation sull'handle
   * Evita che click/pointerdown sull'handle propaghino alla riga
   * e aprano accidentalmente la modale di edit.
   *
   * FIX CRITICO: Dobbiamo chiamare PRIMA il listener di dnd-kit, POI stopPropagation.
   * Se sovrascriviamo onPointerDown senza chiamare listeners.onPointerDown,
   * il drag non parte mai (il listener originale viene sostituito, non esteso).
   */
  const handlePointerDown = (e: React.PointerEvent<HTMLTableCellElement>) => {
    // PRIMA: chiama il listener di dnd-kit per iniziare il drag
    listeners?.onPointerDown?.(e as unknown as React.PointerEvent<Element>);
    // POI: stopPropagation per evitare che il click arrivi alla riga
    e.stopPropagation();
  };

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  return (
    <tr ref={setNodeRef} style={style} className="align-middle">
      {/* Handle drag - chiamiamo manualmente listeners.onPointerDown */}
      <td
        {...attributes}
        onPointerDown={handlePointerDown}
        onClick={handleClick}
        style={{
          width: '40px',
          cursor: isDragDisabled ? 'not-allowed' : 'grab',
          textAlign: 'center',
          userSelect: 'none',
          touchAction: 'none', // Importante per touch devices
        }}
        title={isDragDisabled ? 'Riordino in corso...' : 'Trascina per riordinare'}
      >
        <span style={{ opacity: isDragDisabled ? 0.5 : 1 }}>☰</span>
      </td>

      {/* Numero riga */}
      <td style={{ width: '50px' }}>
        <Badge bg="secondary">{index + 1}</Badge>
      </td>

      {/* Fase lavoro - cliccabile */}
      <td
        onClick={() => onRowClick(dettaglio)}
        style={{ cursor: 'pointer' }}
        className="text-primary"
      >
        {dettaglio.fk_faselavoro_descrizione || `Fase ID: ${dettaglio.fk_faselavoro}`}
      </td>

      {/* Tipo */}
      <td style={{ width: '100px' }}>
        <Badge bg={dettaglio.is_interna ? 'success' : 'warning'}>
          {dettaglio.is_interna ? 'Interna' : 'Esterna'}
        </Badge>
      </td>

      {/* Fornitore */}
      <td>
        {!dettaglio.is_interna && dettaglio.fk_fornitore_nome
          ? dettaglio.fk_fornitore_nome
          : '-'}
      </td>

      {/* Caratteristiche count */}
      <td style={{ width: '80px' }}>
        <Badge bg="info">{dettaglio.caratteristiche_count || 0}</Badge>
      </td>

      {/* Note */}
      <td
        className="text-truncate"
        style={{ maxWidth: '150px' }}
        title={dettaglio.note || ''}
      >
        {dettaglio.note || '-'}
      </td>

      {/* Azioni */}
      <td style={{ width: '100px' }}>
        <ButtonGroup size="sm">
          <Button
            variant="outline-primary"
            onClick={() => onRowClick(dettaglio)}
            title="Modifica"
          >
            ✎
          </Button>
          <Button
            variant="outline-danger"
            onClick={() => onDelete(dettaglio.id)}
            disabled={deleting === dettaglio.id}
            title="Elimina"
          >
            {deleting === dettaglio.id ? '...' : '✕'}
          </Button>
        </ButtonGroup>
      </td>
    </tr>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function DettagliTable({
  proceduraId,
  dettagli,
  onDettagliChange,
  onRowClick,
  onAddClick,
}: DettagliTableProps) {
  const [deleting, setDeleting] = useState<number | null>(null);
  const [isReordering, setIsReordering] = useState(false);

  // Sensors con distance constraint
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  // Delete handler
  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa riga e tutte le sue caratteristiche?')) return;
    try {
      setDeleting(id);
      await deleteDettaglio(id);
      const newDettagli = dettagli.filter((d) => d.id !== id);
      onDettagliChange(newDettagli);
      toast.success('Riga eliminata');
    } catch {
      toast.error('Errore eliminazione riga');
    } finally {
      setDeleting(null);
    }
  };

  /**
   * REORDER con optimistic update + rollback
   *
   * HARDENING: usa backup locale (const) invece di state
   * per evitare stale closure nel catch.
   */
  const handleReorder = async (newDettagli: DettaglioProcedura[]) => {
    // BACKUP LOCALE - catturato PRIMA di qualsiasi modifica
    const backup = [...dettagli];

    // Optimistic update
    onDettagliChange(newDettagli);
    setIsReordering(true);

    try {
      const orderedIds = newDettagli.map((d) => d.id);
      const response = await reorderDettagliProcedura(proceduraId, orderedIds);

      /**
       * SYNC con response API:
       * L'API ritorna DettaglioProcedura[] con numero_riga aggiornato.
       * Usiamo la response per sincronizzare lo state con i dati server.
       */
      if (response.data && Array.isArray(response.data)) {
        onDettagliChange(response.data);
      }
      // Se API non ritorna array, l'ordine locale è già corretto
    } catch {
      // ROLLBACK: usa backup locale (no stale closure)
      toast.error('Errore riordino, ripristinato ordine precedente');
      onDettagliChange(backup);
    } finally {
      setIsReordering(false);
    }
  };

  // Drag end handler
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over || active.id === over.id) return;

    const oldIndex = dettagli.findIndex((d) => d.id === active.id);
    const newIndex = dettagli.findIndex((d) => d.id === over.id);

    if (oldIndex === -1 || newIndex === -1) return;

    const newDettagli = arrayMove(dettagli, oldIndex, newIndex);
    handleReorder(newDettagli);
  };

  return (
    <div>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">
          Righe Procedura
          {dettagli.length > 0 && (
            <Badge bg="secondary" className="ms-2">
              {dettagli.length}
            </Badge>
          )}
          {isReordering && (
            <Spinner animation="border" size="sm" className="ms-2" />
          )}
        </h5>
        <Button variant="primary" size="sm" onClick={onAddClick}>
          + Aggiungi Riga
        </Button>
      </div>

      {/* Table */}
      {dettagli.length === 0 ? (
        <p className="text-muted">
          Nessuna riga. Clicca "Aggiungi Riga" per iniziare.
        </p>
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
                  <th style={{ width: '50px' }}>#</th>
                  <th>Fase Lavoro</th>
                  <th style={{ width: '100px' }}>Tipo</th>
                  <th>Fornitore</th>
                  <th style={{ width: '80px' }}>Caratt.</th>
                  <th>Note</th>
                  <th style={{ width: '100px' }}>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {dettagli.map((d, idx) => (
                  <SortableRow
                    key={d.id}
                    dettaglio={d}
                    index={idx}
                    onRowClick={onRowClick}
                    onDelete={handleDelete}
                    deleting={deleting}
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

/**
 * GenericTableCard - Componente riutilizzabile per card tabella generica.
 *
 * Supporta: ricerca locale, aggiungi (modal), modifica inline, elimina con conferma.
 */
import { useEffect, useState } from 'react';
import {
  Table, Button, Form, InputGroup, Spinner, Modal,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import ConfirmModal from '@/components/common/ConfirmModal';

interface Column<T> {
  header: string;
  accessor: keyof T;
}

interface GenericTableCardProps<T extends { id: number }> {
  columns: Column<T>[];
  fetchFn: (params?: Record<string, unknown>) => Promise<{ data: { results: T[] } }>;
  createFn: (data: Record<string, unknown>) => Promise<unknown>;
  updateFn: (id: number, data: Record<string, unknown>) => Promise<unknown>;
  deleteFn: (id: number) => Promise<unknown>;
  /** Campi del form modale: [{ name, label, required? }] */
  formFields: { name: string; label: string; required?: boolean }[];
  searchPlaceholder?: string;
  searchKey?: keyof T;
  entityName?: string;
}

export default function GenericTableCard<T extends { id: number }>({
  columns,
  fetchFn,
  createFn,
  updateFn,
  deleteFn,
  formFields,
  searchPlaceholder = 'Cerca...',
  searchKey,
  entityName = 'elemento',
}: GenericTableCardProps<T>) {
  const [items, setItems] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);

  // Modal state
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<T | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetchFn({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore durante il caricamento');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteFn(id);
      toast.success(`${entityName} eliminato`);
      fetchData();
    } catch {
      toast.error(`Errore nell'eliminazione`);
    }
    setDeleteId(null);
  };

  const openCreate = () => {
    setEditingItem(null);
    const empty: Record<string, string> = {};
    formFields.forEach((f) => { empty[f.name] = ''; });
    setFormData(empty);
    setShowModal(true);
  };

  const openEdit = (item: T) => {
    setEditingItem(item);
    const data: Record<string, string> = {};
    formFields.forEach((f) => {
      data[f.name] = String((item as Record<string, unknown>)[f.name] ?? '');
    });
    setFormData(data);
    setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editingItem) {
        await updateFn(editingItem.id, formData);
        toast.success(`${entityName} aggiornato`);
      } else {
        await createFn(formData);
        toast.success(`${entityName} creato`);
      }
      setShowModal(false);
      fetchData();
    } catch {
      toast.error('Errore nel salvataggio');
    } finally {
      setSaving(false);
    }
  };

  const filtered = items.filter((item) => {
    if (!search || !searchKey) return true;
    const val = String((item as Record<string, unknown>)[searchKey as string] ?? '');
    return val.toLowerCase().includes(search.toLowerCase());
  });

  return (
    <>
      <InputGroup className="mb-2" size="sm">
        <Form.Control
          placeholder={searchPlaceholder}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={openCreate}>
          + Aggiungi
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-3"><Spinner size="sm" /></div>
      ) : (
        <Table size="sm" striped hover responsive>
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={String(c.accessor)}>{c.header}</th>
              ))}
              <th className="text-end">Azioni</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={columns.length + 1} className="text-muted text-center">Nessun elemento</td></tr>
            ) : (
              filtered.map((item) => (
                <tr key={item.id}>
                  {columns.map((c) => (
                    <td key={String(c.accessor)}>
                      {String((item as Record<string, unknown>)[c.accessor as string] ?? '—')}
                    </td>
                  ))}
                  <td className="text-end text-nowrap">
                    <Button
                      size="sm" variant="outline-primary" className="me-1"
                      onClick={() => openEdit(item)}
                    >
                      ✏️
                    </Button>
                    <Button
                      size="sm" variant="outline-danger"
                      onClick={() => setDeleteId(item.id)}
                    >
                      🗑
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      )}

      {/* Modal Aggiungi/Modifica */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingItem ? `Modifica ${entityName}` : `Nuovo ${entityName}`}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {formFields.map((f) => (
            <Form.Group key={f.name} className="mb-3">
              <Form.Label>{f.label}</Form.Label>
              <Form.Control
                value={formData[f.name] || ''}
                onChange={(e) => setFormData((prev) => ({ ...prev, [f.name]: e.target.value }))}
                required={f.required}
              />
            </Form.Group>
          ))}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Annulla
          </Button>
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? <Spinner size="sm" /> : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>

      <ConfirmModal
        show={!!deleteId}
        onHide={() => setDeleteId(null)}
        onConfirm={() => deleteId && handleDelete(deleteId)}
        message={`Sei sicuro di voler eliminare questo ${entityName}?`}
      />
    </>
  );
}

/**
 * TabelleGenericheHRPage - Gestione tabelle di lookup HR
 *
 * - Centri di Lavoro
 * - Reparti (Ward)
 * - Mansioni (Role)
 */
import { useState, useEffect, useCallback } from 'react';
import {
  Card,
  Tabs,
  Tab,
  Table,
  Button,
  Spinner,
  Modal,
  Form,
  Row,
  Col,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getCentriDiLavoro,
  createCentroDiLavoro,
  updateCentroDiLavoro,
  deleteCentroDiLavoro,
  getReparti,
  createReparto,
  updateReparto,
  deleteReparto,
  getMansioni,
  createMansione,
  updateMansione,
  deleteMansione,
} from '../api';
import type { CentrodiLavoro, Ward, Role } from '../types';

export default function TabelleGenericheHRPage() {
  const [activeTab, setActiveTab] = useState('centri');

  return (
    <Card>
      <Card.Header>
        <strong>Tabelle Generiche - Human Resources</strong>
      </Card.Header>
      <Card.Body>
        <Tabs
          activeKey={activeTab}
          onSelect={(k) => setActiveTab(k || 'centri')}
          className="mb-4"
        >
          <Tab eventKey="centri" title="Centri di Lavoro">
            <CentriDiLavoroSection />
          </Tab>
          <Tab eventKey="reparti" title="Reparti">
            <RepartiSection />
          </Tab>
          <Tab eventKey="mansioni" title="Mansioni">
            <MansioniSection />
          </Tab>
        </Tabs>
      </Card.Body>
    </Card>
  );
}

// =============================================================================
// CENTRI DI LAVORO SECTION
// =============================================================================

function CentriDiLavoroSection() {
  const [items, setItems] = useState<CentrodiLavoro[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<CentrodiLavoro | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getCentriDiLavoro({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento centri di lavoro');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setShowModal(true);
  };

  const handleEdit = (item: CentrodiLavoro) => {
    setEditing(item);
    setFormDescription(item.description);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateCentroDiLavoro(editing.id, { description: formDescription.trim() });
        toast.success('Centro di lavoro aggiornato');
      } else {
        await createCentroDiLavoro({ description: formDescription.trim() });
        toast.success('Centro di lavoro creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: CentrodiLavoro) => {
    if (!confirm(`Eliminare "${item.description}"?`)) return;
    try {
      setDeleting(item.id);
      await deleteCentroDiLavoro(item.id);
      toast.success('Centro di lavoro eliminato');
      await loadItems();
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare il centro di lavoro. Potrebbe essere in uso.';
      toast.error(msg);
    } finally {
      setDeleting(null);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <p className="text-muted mb-0">
          I centri di lavoro sono utilizzati per le valutazioni degli operatori.
        </p>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Nuovo Centro
        </Button>
      </div>

      <Table striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th style={{ width: '120px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.description}</td>
              <td>
                <Button
                  variant="outline-primary"
                  size="sm"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  Modifica
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(item)}
                  disabled={deleting === item.id}
                >
                  {deleting === item.id ? <Spinner animation="border" size="sm" /> : 'Elimina'}
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={2} className="text-center text-muted">
                Nessun centro di lavoro presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Centro di Lavoro' : 'Nuovo Centro di Lavoro'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group>
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                required
                autoFocus
              />
            </Form.Group>
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

// =============================================================================
// REPARTI SECTION
// =============================================================================

function RepartiSection() {
  const [items, setItems] = useState<Ward[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Ward | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getReparti({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento reparti');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setShowModal(true);
  };

  const handleEdit = (item: Ward) => {
    setEditing(item);
    setFormDescription(item.description);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateReparto(editing.id, { description: formDescription.trim() });
        toast.success('Reparto aggiornato');
      } else {
        await createReparto({ description: formDescription.trim() });
        toast.success('Reparto creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: Ward) => {
    if (!confirm(`Eliminare "${item.description}"?`)) return;
    try {
      setDeleting(item.id);
      await deleteReparto(item.id);
      toast.success('Reparto eliminato');
      await loadItems();
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare il reparto. Potrebbe essere associato a dipendenti o mansioni.';
      toast.error(msg);
    } finally {
      setDeleting(null);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <p className="text-muted mb-0">
          I reparti sono utilizzati per organizzare i dipendenti.
        </p>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Nuovo Reparto
        </Button>
      </div>

      <Table striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th style={{ width: '120px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.description}</td>
              <td>
                <Button
                  variant="outline-primary"
                  size="sm"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  Modifica
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(item)}
                  disabled={deleting === item.id}
                >
                  {deleting === item.id ? <Spinner animation="border" size="sm" /> : 'Elimina'}
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={2} className="text-center text-muted">
                Nessun reparto presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Reparto' : 'Nuovo Reparto'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group>
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                required
                autoFocus
              />
            </Form.Group>
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

// =============================================================================
// MANSIONI SECTION
// =============================================================================

function MansioniSection() {
  const [items, setItems] = useState<Role[]>([]);
  const [reparti, setReparti] = useState<Ward[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Role | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [formReparto, setFormReparto] = useState<number | ''>('');
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const [mansioniRes, repartiRes] = await Promise.all([
        getMansioni({ page_size: 1000 }),
        getReparti({ page_size: 1000 }),
      ]);
      setItems(mansioniRes.data.results);
      setReparti(repartiRes.data.results);
    } catch {
      toast.error('Errore caricamento mansioni');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setFormReparto('');
    setShowModal(true);
  };

  const handleEdit = (item: Role) => {
    setEditing(item);
    setFormDescription(item.description);
    setFormReparto(item.fk_reparto || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      const data = {
        description: formDescription.trim(),
        fk_reparto: formReparto ? (formReparto as number) : null,
      };
      if (editing) {
        await updateMansione(editing.id, data);
        toast.success('Mansione aggiornata');
      } else {
        await createMansione(data);
        toast.success('Mansione creata');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: Role) => {
    if (!confirm(`Eliminare "${item.description}"?`)) return;
    try {
      setDeleting(item.id);
      await deleteMansione(item.id);
      toast.success('Mansione eliminata');
      await loadItems();
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare la mansione. Potrebbe essere associata a dipendenti.';
      toast.error(msg);
    } finally {
      setDeleting(null);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <p className="text-muted mb-0">
          Le mansioni possono essere associate a un reparto.
        </p>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Nuova Mansione
        </Button>
      </div>

      <Table striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>Reparto</th>
            <th style={{ width: '120px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.description}</td>
              <td>{item.fk_reparto_display || '-'}</td>
              <td>
                <Button
                  variant="outline-primary"
                  size="sm"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  Modifica
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(item)}
                  disabled={deleting === item.id}
                >
                  {deleting === item.id ? <Spinner animation="border" size="sm" /> : 'Elimina'}
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={3} className="text-center text-muted">
                Nessuna mansione presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Mansione' : 'Nuova Mansione'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Row>
              <Col md={12}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Descrizione <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    value={formDescription}
                    onChange={(e) => setFormDescription(e.target.value)}
                    required
                    autoFocus
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Reparto (opzionale)</Form.Label>
                  <Form.Select
                    value={formReparto}
                    onChange={(e) =>
                      setFormReparto(e.target.value ? Number(e.target.value) : '')
                    }
                  >
                    <option value="">-- Nessun reparto --</option>
                    {reparti.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.description}
                      </option>
                    ))}
                  </Form.Select>
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
